# captool.py

Experimental functions for generating and transcoding Tahoe-LAFS capabilities. _This code is for learning-purposes only; do not use this for anything important!_

## Examples:

Deterministically generate a new Tahoe-LAFS mutable filecap from a random seed encoded as a [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) mnemonic:
```
$ captool generate
seven kiwi smile mouse uniform ignore hire cup pause filter rare already
URI:MDMF:k5zwakckdre5u3mt3ol45nonsq:ginoan4k74gqv4d53kujgepsthwken63lgu5ct4x4dcmfle5dg4a
URI:MDMF-RO:3nd3blmfqoclylxwuo55caowam:ginoan4k74gqv4d53kujgepsthwken63lgu5ct4x4dcmfle5dg4a
```

Generate/recover the above mutable filecap later from the original mnemonic:
```
$ captool generate seven kiwi smile mouse uniform ignore hire cup pause filter rare already
URI:MDMF:k5zwakckdre5u3mt3ol45nonsq:ginoan4k74gqv4d53kujgepsthwken63lgu5ct4x4dcmfle5dg4a
```

Diminish a read-write mutable filecap to its read-only variant -- without the need to run `tahoe`:
```
$ captool diminish URI:MDMF:kjoqabgevk2roi52dihdoedmm4:x5mbr5a3s2xp5dcq66wjfhxfi3wpq4vl2gjdrja226hn4eqgwbxa
URI:MDMF-RO:iecipe3fa3kbpv3bc7yx5omsci:x5mbr5a3s2xp5dcq66wjfhxfi3wpq4vl2gjdrja226hn4eqgwbxa
```

Convert an existing mutable filecap to a long* mnemonic:
```
$ captool to-words URI:MDMF:xcg6knplnx4frmlxsjzpiywaee:zc2nbbyhm7ugupu5u5pwzj4edbmegolitmo7gmeaeoww44dgn7kq
review hundred estate strategy test clump shift venture indicate perfect quote dumb silly pledge canyon attract leader crush whip reject garage gown three cost loud original pen glove veteran lottery angry food train creek satisfy radio
```
<sub>* This is 36 words long because we must encode the hashes of both the writekey and fingerprint; in this case, we do not have the original RSA private key seed from which both of those components originally derived.</sub>


Convert a (long) mnemonic back to the original mutable filecap:
```
captool to-cap review hundred estate strategy test clump shift venture indicate perfect quote dumb silly pledge canyon attract leader crush whip reject garage gown three cost loud original pen glove veteran lottery angry food train creek satisfy radio                                                                                                                                                                                                     
URI:MDMF:xcg6knplnx4frmlxsjzpiywaee:zc2nbbyhm7ugupu5u5pwzj4edbmegolitmo7gmeaeoww44dgn7kq
```
