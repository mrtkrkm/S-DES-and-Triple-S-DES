from flask import Flask,render_template,request,url_for
from SDES.Cracking import Crack
from SDES.TripleSDES import TripleSDES

app=Flask(__name__)

Key1='1000101110'
Key2='0110101110'

tsd=TripleSDES(Key1,Key2)
crack_m=Crack()
def get_message(cipher_m):
    text=''
    blocks=crack_m.create_blocks(cipher_m)
    for block in blocks:
        plain_b=tsd.decryption(block)
        text +=crack_m.convert_ascii(plain_b)
    return text

@app.route('/', methods=['POST','GET'])
def main():
    text=''

    if request.method=='GET':
        text='Empty'
    if request.method=='POST':
        cipher=request.form['cipherText']
        text=get_message(cipher)

    return render_template('home.html',text=text)


def run():
    app.run(debug=True)

