## BitcoinDiamond-Docker
A BitcoinDiamond Core docker image.
### build

```
cd /BitcoinDiamond/contrib/Docker
docker build -t bcd .
```

### Run

```
docker run -ti --name container_name -v /yourdir:/home/bitcoin/.bitcoindiamond bcd
```

### Exec

```
docker exec --user bitcoin container_name bitcoindiamond-cli getmininginfo
```
### Example

```
 - docker build -t bcd .
 - docker run -ti --name bcd-1 -v /home:/home/bitcoin/.bitcoindiamond bcd -regtest=1
 - docker exec --user bitcoin bcd-1 bitcoindiamond-cli -regtest=1 getmininginfo
	{
		"blocks": 0,
		"currentblocksize": 0,
		"currentblockweight": 0,
		"currentblocktx": 0,
		"difficulty": 1,
		"errors": "",
		"networkhashps": 0,
		"pooledtx": 0,
		"chain": "test"
	}
```

### Reference

 - https://github.com/ruimarinho/docker-bitcoin-core

