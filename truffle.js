/*
 * NB: since truffle-hdwallet-provider 0.0.5 you must wrap HDWallet providers in a 
 * function when declaring them. Failure to do so will cause commands to hang. ex:
 * ```
 * mainnet: {
 *     provider: function() { 
 *       return new HDWalletProvider(mnemonic, 'https://mainnet.infura.io/<infura-key>') 
 *     },
 *     network_id: '1',
 *     gas: 4500000,
 *     gasPrice: 10000000000,
 *   },
 */

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  networks: {
      roptest: {
          host: "localhost",
          port: 8545,
          network_id: "3",
          gas: 6000000,
          gasPrice: 4000000000,
          from: "0x8f106d3e03ccb8042772261661789445fd9d930a"
      },
      mytest: {
          host: "127.0.0.1",
          port: 8090,
          network_id: "666",
          gas: 7000000,
          gasPrice: 4000000000,
          from: "0x09de6b21f6c115871e6440ece7950fe26b6764fd"
      },
      private_test: {
          host: "101.37.115.57",
          port: 18090,
          network_id: "666",
          gas: 7000000,
          gasPrice: 4000000000,
          from: "0xc65add7b33dd1203181e3802d2374391ba68dd69"
      }
  }
};
