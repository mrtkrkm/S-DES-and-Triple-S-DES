Required libraries:
click==7.1.2
Flask==1.1.2
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1


This project consist of 3 packages and one main python file. 
- Flask Web
   - static
   - templates
   - flask_main.py
- PolyAlphabeticCipher
   - Constants
   - PolyAlph.py
- SDES.
   - Constants
   - S_DES.py
   - TripleSDES.py
   - Cracking.py
- main.py


```
###TASK 3 ###
crack_ins=crack()
crack_ins.crack_sdes('data/ctx1.txt')
crack_ins.crack_tsdes('data/ctx1.txt')
```

The block above show the Part 2- Task 3 codes. It calls the Cracking.py file in the main.py and do necessary calculation.



