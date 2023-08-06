import os
import hashlib

from populus.utils.filesystem import (
    get_contracts_dir,
    get_build_dir,
    get_compiled_contracts_file_path,
    get_blockchains_dir,
    get_migrations_dir,
    relpath,
)
from populus.utils.chains import (
    get_data_dir,
    get_chaindata_dir,
    get_dapp_dir,
    get_geth_ipc_path,
    get_nodekey_path,
)
from populus.utils.config import (
    get_default_project_config_file_path,
    find_project_config_file_path,
)

from populus.migrations.migration import (
    sort_migrations,
)
from populus.migrations.loading import (
    find_project_migrations,
    load_project_migrations,
)
from populus.compilation import (
    find_project_contracts,
    compile_project_contracts,
)
from populus.config import (
    load_config as _load_config,
    write_config as _write_config,
    load_default_config_info,
    Config,
)
from populus.chain import (
    TestRPCChain,
    EthereumTesterChain,
    TemporaryGethChain,
    MordenChain,
    MainnetChain,
    LocalGethChain,
    ExternalChain,
)


class Project(object):
    def __init__(self, config_file_path=None):
        if config_file_path is None:
            try:
                config_file_path = find_project_config_file_path()
            except ValueError:
                pass
        self.config_file_path = config_file_path
        self.load_config()

    #
    # Config
    #
    config_file_path = None

    _project_config = None
    _default_config_info = None

    def write_config(self):
        if self.config_file_path is None:
            config_file_path = get_default_project_config_file_path(self.project_dir)
        else:
            config_file_path = self.config_file_path

        self.config_file_path = _write_config(
            self.project_dir,
            self.config.config_for_write,
            write_path=config_file_path,
        )

        return self.config_file_path

    def load_config(self):
        self._config_cache = None

        if self.config_file_path:
            self._project_config = _load_config(self.config_file_path)

        self._default_config_info = load_default_config_info()

    def reload_config(self):
        self.load_config()

    _config_cache = None

    @property
    def config(self):
        if self._config_cache is None:
            self._config_cache = Config(self._project_config, self._default_config_info)
        return self._config_cache

    #
    # Project
    #
    @property
    def project_dir(self):
        return self.config.get('populus.project_dir', os.getcwd())

    #
    # Contracts
    #
    @property
    @relpath
    def contracts_dir(self):
        if 'compilation.contracts_dir' in self.config:
            return self.config['compilation.contracts_dir']
        else:
            return get_contracts_dir(self.project_dir)

    @property
    @relpath
    def build_dir(self):
        if 'compilation.build_dir' in self.config:
            return self.config['compilation.build_dir']
        else:
            return get_build_dir(self.project_dir)

    @property
    @relpath
    def compiled_contracts_file_path(self):
        return get_compiled_contracts_file_path(self.project_dir)

    _cached_compiled_contracts_mtime = None
    _cached_compiled_contracts = None

    def get_source_file_hash(self):
        source_file_paths = find_project_contracts(self.project_dir, self.contracts_dir)
        return hashlib.md5(b''.join(
            open(source_file_path, 'rb').read()
            for source_file_path
            in source_file_paths
        )).hexdigest()

    def get_source_modification_time(self):
        source_file_paths = find_project_contracts(self.project_dir, self.contracts_dir)
        return max(
            os.path.getmtime(source_file_path)
            for source_file_path
            in source_file_paths
        ) if len(source_file_paths) > 0 else None

    def compiled_contracts_stale(self):
        return self._cached_compiled_contracts_mtime is None or \
            self._cached_compiled_contracts_mtime < self.get_source_modification_time()

    def fill_contracts_cache(self, contracts, contracts_mtime):
        """
        :param contracts: become the Project's cache for compiled contracts
        :param contracts_mtime: last modification of supplied contracts
        :return:
        """
        self._cached_compiled_contracts_mtime = contracts_mtime
        self._cached_compiled_contracts = contracts

    @property
    def compiled_contracts(self):
        if self.compiled_contracts_stale():
            self._cached_compiled_contracts_mtime = self.get_source_modification_time()
            # TODO: the hard coded `optimize=True` should be configurable
            # somehow.
            _, self._cached_compiled_contracts = compile_project_contracts(
                project_dir=self.project_dir,
                contracts_dir=self.contracts_dir,
                optimize=True,
            )
        return self._cached_compiled_contracts

    #
    # Local Blockchains
    #
    def get_chain_config(self, chain_name):
        chain_config_key = 'chains.{chain_name}'.format(chain_name=chain_name)

        if chain_config_key in self.config:
            return self.config.get_config(chain_config_key)
        else:
            raise KeyError(
                "Unknown chain: {0!r} - Must be one of {1!r}".format(
                    chain_name,
                    sorted(self.config.get('chains', {}).keys()),
                )
            )

    def get_chain(self, chain_name, *chain_args, **chain_kwargs):
        """
        Returns a context manager that runs a chain within the context of the
        current populus project.

        Support pre-configured chain names:

        - 'testrpc': Chain backed by an ephemeral eth-testrpc chain.
        - 'tester': Chain backed by an ephemeral ethereum.tester chain.
        - 'temp': Chain backed by geth running a local chain in a temporary
          directory that will be automatically deleted when the chain shuts down.
        - 'mainnet': Chain backed by geth running against the public mainnet.
        - 'morden': Chain backed by geth running against the public morden
          testnet.

        Alternatively you can specify any of the pre-configured chains from the
        project's populus.ini configuration file.

        All geth backed chains are subject to up to 10 minutes of wait time
        during first boot to generate the DAG file if the chain configured to
        mine.

        * See https://github.com/ethereum/wiki/wiki/Ethash-DAG
        * These are shared across all Ethereum nodes and live in
          ``$(HOME)/.ethash/`` folder

        To avoid this long wait time, you can manuall pre-generate the DAG with
        ``$ geth makedag 0 $HOME/.ethash``

        Example:

        .. code-block:: python

            >>> from populus.project import default_project as my_project
            >>> with my_project.get_chain('testrpc') as chain:
            ...     web3 = chain.web3
            ...     MyContract = chain.contract_factories.MyContract
            ...     # do things


        :param chain_name: The name of the chain that should be returned
        :param chain_args: Positional arguments that should be passed into the
                           chain constructor.
        :param chain_kwargs: Named arguments that should be passed into the
                             constructor

        :return: :class:`populus.chain.Chain`
        """
        if chain_name == 'testrpc':
            return TestRPCChain(self, 'testrpc', *chain_args, **chain_kwargs)
        elif chain_name == 'tester':
            return EthereumTesterChain(self, 'tester', *chain_args, **chain_kwargs)
        elif chain_name == 'temp':
            return TemporaryGethChain(self, 'temp', *chain_args, **chain_kwargs)

        chain_config = self.get_chain_config(chain_name)

        if chain_config.get('is_external', False):
            # TODO: the chain_kwargs is really currently required to contain a
            # `web3` instance.  This isn't quite congruent with the current
            # API.
            return ExternalChain(self, chain_name, *chain_args, **chain_kwargs)

        if chain_name == 'morden':
            return MordenChain(self, 'morden', *chain_args, **chain_kwargs)
        elif chain_name == 'mainnet':
            return MainnetChain(self, 'mainnet', *chain_args, **chain_kwargs)
        else:
            return LocalGethChain(self,
                                  chain_name=chain_name,
                                  *chain_args,
                                  **chain_kwargs)

    @property
    @relpath
    def blockchains_dir(self):
        return get_blockchains_dir(self.project_dir)

    @relpath
    def get_blockchain_data_dir(self, chain_name):
        return get_data_dir(self.project_dir, chain_name)

    @relpath
    def get_blockchain_chaindata_dir(self, chain_name):
        return get_chaindata_dir(self.get_blockchain_data_dir(chain_name))

    @relpath
    def get_blockchain_dapp_dir(self, chain_name):
        return get_dapp_dir(self.get_blockchain_data_dir(chain_name))

    @relpath
    def get_blockchain_ipc_path(self, chain_name):
        return get_geth_ipc_path(self.get_blockchain_data_dir(chain_name))

    @relpath
    def get_blockchain_nodekey_path(self, chain_name):
        return get_nodekey_path(self.get_blockchain_data_dir(chain_name))

    #
    # Migrations
    #
    @property
    @relpath
    def migrations_dir(self):
        return get_migrations_dir(self.project_dir)

    @property
    def migration_files(self):
        return list((
            os.path.relpath(migration_file_path)
            for migration_file_path
            in sorted(find_project_migrations(self.project_dir))
        ))

    @property
    def migrations(self):
        return sort_migrations(
            load_project_migrations(self.project_dir),
            flatten=True,
        )
