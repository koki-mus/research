from types import MethodDescriptorType
from flask import Flask, jsonify,request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

@app.route("/postdata", methods=["POST"])
def writedata():
    response = jsonify({"token":"dummy"})
    req = request.json[0]
    try:
        with open(req["filepath"], "a") as f:
            # f.write(str(request.json[0]))
            #{'snappath': './snap49/lic_snap49.52.03.bmp',
            # 'filepath': '../txt/test.csv
            #  'locnumx': 0, 'locnumy': 0,
            #  'locnumx2': 0, 'locnumy2': 0,
            #  'rangenumx': 0, 'rangenumy': 0}
            doc = str(request.json[0])
            f.write(doc)
        return "Succes"
    except FileNotFoundError:
        return "File not Found"
    except:
        return "failed"

@app.route("/", methods=["post"])
def postf():
    # request.form["token"] #
    response = jsonify({"token":"dummy"})
    return response

print("ss")
app.run(host="127.0.0.1", port=8888, debug=True)