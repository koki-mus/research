#bmpが入っているディレクトリの親ディレクトリで実行してください
import glob
from mymodule import myfunc as mf
def main():
    dataset = input("which dataset:")
    outname = f"lic_viewer{dataset}.html"
    paths = glob.glob(f"./snap{dataset}/*bmp")
    paths = mf.sort_paths(paths)
    part1 = '<!DOCTYPE html>\n\
    <html>\n\
    <head>\n\
        <title>viewer</title>\n\
    </head>\n\
    <body>\n\
        <div class="navi">\n\
                <input type="button" value=" 100戻る(A)" onclick="move(-100);"/>\n\
            <input type="button" value=" 10戻る(S)" onclick="move(-10);"/>\n\
            <input type="button" value=" 1戻る(D)" onclick="move(-1);"/>\n\
            <input type="button" value="1進む(F)" onclick="move(1);"/>\n\
            <input type="button" value="10進む(G)" onclick="move(10);"/>\n\
            <input type="button" value="100進む(H)" onclick="move(100);"/>\n\
        </div>\n\
        <p id="currentpath"></p>\n\
        <div class="imgcvs">\n\
            <canvas class="cv" id="cvx"></canvas>\n\
            <canvas class="cv" id="cvy"></canvas>\n\
            <canvas class="cv" id="box"></canvas>\n\
            <img id="output" src=""><br><br>\n\
        </div>\n\
        <br/>\n\
        <p class="discribe">グリッド: x方向の幅</p><input class="textinput" id="dxinput" type="text" name="text" value="30">\n\
        <p class="discribe">y方向の幅</p><input class="textinput" id="dyinput" type="text" name="text" value="30">\n\
        <p>元データのピクセルに準拠</p>\n\
        <p class="discribe">範囲の描画</p>\n\
        <p class="discribe">始点X</p><input class="boxinput textinput" id="box1" type="text" value="30">\n\
        <p class="discribe">始点Y</p><input class="boxinput textinput" id="box2" type="text"value="30">\n\
        <p class="discribe">終点X</p><input class="boxinput textinput" id="box3" type="text"value="100">\n\
        <p class="discribe">終点Y</p><input class="boxinput textinput" id="box4" type="text" value="100">\n\
\n\
    </body>\n\
    </html>\n\
    <script language="javascript" type="text/javascript">\n\
        var path_index = 0\n\
        var paths =['
    part2 = ']\n\
        function update(){\n\
            target = document.getElementById("output");\n\
            target.setAttribute("src", paths[path_index]);\n\
            document.getElementById("currentpath").innerHTML = paths[path_index];\n\
            // document.getElementById(currentpath).setAttribute("txt",paths[path_index]);\n\
        }\n\
        update()\n\
        function move(num){\n\
            temp = path_index +num;\n\
            if (0 <= temp && temp < paths.length) {\n\
                path_index = temp;\n\
                update();\n\
            }\n\
        }\n\
        var cvsx = document.getElementById("cvx");\n\
        var cvsy = document.getElementById("cvy");\n\
        var boxs = document.getElementById("box")\n\
        const imgXlen = 1799;\n\
        const imgYlen = 570;\n\
        cvsx.setAttribute( "width" , imgXlen);\n\
        cvsx.setAttribute( "height" , imgYlen);\n\
        cvsy.setAttribute( "width" , imgXlen);\n\
        cvsy.setAttribute( "height" , imgYlen);\n\
        boxs.setAttribute( "width" , imgXlen);\n\
        boxs.setAttribute( "height" , imgYlen);\n\
        var ctxx = cvsx.getContext("2d");\n\
        var ctxy = cvsy.getContext("2d");\n\
        var boxct = boxs.getContext("2d");\n\
        function drawlinex(startx,starty,endx,endy){\n\
            ctxx.beginPath();\n\
            ctxx.lineWidth = 0.8;\n\
            ctxx.strokeStyle = "rgba(0,0,255,0.8)"\n\
            ctxx.moveTo(startx, starty);\n\
            ctxx.lineTo(endx,endy);\n\
            ctxx.stroke()\n\
        }\n\
        function drawliney(startx,starty,endx,endy){\n\
            ctxy.beginPath();\n\
            ctxy.lineWidth = 0.8;\n\
            ctxy.strokeStyle = "rgba(64,64,255,0.5)"\n\
            ctxy.moveTo(startx, starty);\n\
            ctxy.lineTo(endx,endy);\n\
            ctxy.stroke()\n\
        }\n\
        const orgx = 257;\n\
        const orgy = 1025;\n\
        const inputx = document.getElementById("dxinput");\n\
        function drawglidx(){\n\
            ctxx.clearRect(0,0,imgXlen,imgYlen)\n\
            inputdx = Number(document.getElementById("dxinput").value);\n\
            if (inputdx <0.2) {\n\
                return 0\n\
            }\n\
            dx = inputdx*imgXlen/orgx\n\
            for (let index = 0; index*dx < imgXlen; index++) {\n\
                drawlinex(index*dx, 0,index*dx, imgXlen)\n\
            }\n\
        }\n\
\n\
        const inputy = document.getElementById("dyinput");\n\
        function drawglidy(){\n\
            ctxy.clearRect(0,0,imgXlen,imgYlen)\n\
            inputdy = Number(document.getElementById("dyinput").value);\n\
            if (inputdy <0.2) {\n\
                return 0;\n\
            }\n\
            dy = inputdy*imgYlen/orgy;\n\
            for (let index = 0; index*dy < imgYlen; index++) {\n\
            drawliney(0,index*dy, imgXlen,index*dy);\n\
        }\n\
        }\n\
        drawglidx()\n\
        drawglidy()\n\
        inputx.addEventListener("input", drawglidx);\n\
        inputy.addEventListener("input", drawglidy);\n\
\n\
        const box1 = document.getElementById("box1");\n\
        const box2 = document.getElementById("box2");\n\
        const box3 = document.getElementById("box3");\n\
        const box4 = document.getElementById("box4");\n\
        function drawbox(){\n\
            boxct.clearRect(0,0,imgXlen,imgYlen)\n\
            boxct.lineWidth = 2;\n\
            boxct.strokeStyle = "rgba(255,64,64,1)"\n\
            var num1 = Number(box1.value)*imgXlen/orgx\n\
            var num2 = Number(box2.value)*imgYlen/orgy\n\
            var num3 = Number(box3.value)*imgXlen/orgx\n\
            var num4 = Number(box4.value)*imgYlen/orgy\n\
            console.log(num1)\n\
            boxct.beginPath();\n\
            boxct.moveTo(num1, num2);\n\
            boxct.lineTo(num3, num2);\n\
            boxct.lineTo(num3, num4);\n\
            boxct.lineTo(num1, num4);\n\
            boxct.closePath()\n\
            boxct.stroke()\n\
        }\n\
\n\
        box1.addEventListener("input", drawbox);\n\
        box2.addEventListener("input", drawbox);\n\
        box3.addEventListener("input", drawbox);\n\
        box4.addEventListener("input", drawbox);\n\
                    document.addEventListener("keypress", keypress_ivent);\n\
        function keypress_ivent(e) {\n\
            if(e.key === "a" || e.key === "A"){\n\
                move(-100)\n\
            }else if(e.key === "s" || e.key === "S"){\n\
                move(-10)\n\
            }else if(e.key === "d" || e.key === "D"){\n\
                move(-1)\n\
            }else if(e.key === "f" || e.key === "F"){\n\
                move(1)\n\
            }else if(e.key === "g" || e.key === "G"){\n\
                move(10)\n\
            }else if(e.key === "h" || e.key === "H"){\n\
                move(100)\n\
            }\n\
            return false; \n\
        }\n\
      </script>\n\
      <style>\n\
        body{\n\
            padding-left: 30px;\n\
            padding-top: 30px;\n\
            text-align: center;\n\
        }\n\
        .navi input{\n\
            display: inline;\n\
            width: 74px;\n\
            height: 30px;\n\
            margin: 0px;\n\
            padding: 0px;\n\
        }\n\
        .navi{\n\
            position: fixed;\n\
            z-index: 1;\n\
            height: 50px;\n\
            top: 10px;\n\
        }\n\
        .cv{\n\
            width:1799px;\n\
            height: 570px;\n\
            position: absolute;\n\
        }\n\
        .img{\n\
            width: 1799px;\n\
            height: 570px;\n\
            position: absolute;\n\
        }\n\
        .discribe{\n\
            display: inline;\n\
        }\n\
        .textinput{\n\
            width: 30px;\n\
            text-align: right;\n\
        }\n\
      </style>\n\
    '

    for p in paths:
        tempstr = p.replace("\\","/")
        part1 += f"'{tempstr}',\n"
    all = part1+part2
    with open(outname, "w", encoding="utf8") as f:
        f.write(all)

if __name__ == '__main__':
    main()