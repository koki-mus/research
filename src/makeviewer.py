#bmpが入っているディレクトリの親ディレクトリで実行してください
import glob
from mymodule import myfunc as mf
def main():
    outname = "lic_viewer49.html"
    paths = glob.glob("./snap49/*bmp")
    paths = mf.sort_paths(paths)
    part1 = '<!DOCTYPE html>\n\
    <html>\n\
    <head>\n\
        <title>viewer</title>\n\
    </head>\n\
    <body>\n\
        <p id="currentpath"></p>\n\
        <div class="imgcvs">\n\
            <canvas class="cv" id="cvx"></canvas>\n\
            <canvas class="cv" id="cvy"></canvas>\n\
            <img id="output" src=""><br><br>\n\
        </div>\n\
            <div class="navi">\n\
                <input type="button" value=" 100進む" onclick="move(-100);"/>\n\
            <input type="button" value=" 10進む" onclick="move(-10);"/>\n\
            <input type="button" value=" 1進む" onclick="move(-1);"/>\n\
            <input type="button" value="1戻る" onclick="move(1);"/>\n\
            <input type="button" value="10戻る" onclick="move(10);"/>\n\
            <input type="button" value="100戻る" onclick="move(100);"/>\n\
        </div>\n\
        <br/>\n\
        <p class="discribe">x方向の幅</p><input id="dxinput" type="text" name="text" value="30">\n\
        <p class="discribe">y方向の幅</p><input id="dyinput" type="text" name="text" value="30">\n\
        <p>元データのピクセルに準拠</p>\n\
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
        const imgXlen = 1799;\n\
        const imgYlen = 570;\n\
        cvsx.setAttribute( "width" , imgXlen);\n\
        cvsx.setAttribute( "height" , imgYlen);\n\
        cvsy.setAttribute( "width" , imgXlen);\n\
        cvsy.setAttribute( "height" , imgYlen);\n\
        var ctxx = cvsx.getContext("2d");\n\
        var ctxy = cvsy.getContext("2d");\n\
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
\n\
        // dy = 60*imgYlen/orgy;\n\
        // for (let index = 0; index*dy < imgYlen; index++) {\n\
        //     drawline(0,index*dy, imgXlen,index*dy)\n\
        //     console.log(index*dy)\n\
        // }\n\
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
                console.log(index*dx)\n\
            }\n\
        }\n\
\n\
        const inputy = document.getElementById("dyinput");\n\
        function drawglidy(){\n\
            ctxy.clearRect(0,0,imgXlen,imgYlen)\n\
            inputdy = Number(document.getElementById("dyinput").value);\n\
            if (inputdy <0.2) {\n\
                return 0\n\
            }\n\
            dy = inputdy*imgYlen/orgy\n\
            for (let index = 0; index*dy < imgYlen; index++) {\n\
            drawliney(0,index*dy, imgXlen,index*dy)\n\
            console.log(index*dy)\n\
        }\n\
        }\n\
        drawglidx()\n\
        drawglidy()\n\
        inputx.addEventListener("input", drawglidx);\n\
        inputy.addEventListener("input", drawglidy);\n\
      </script>\n\
      <style>\n\
        body{\n\
            padding-left: 30px;\n\
            padding-top: 30px;\n\
            text-align: center;\n\
        }\n\
        .navi input{\n\
            display: inline;\n\
            width: 65px\n\
        }\n\
        .cv{\n\
            width:1799px;\n\
            height: 570px;\n\
            position: absolute;\n\
        }\n\
        .img{\n\
            width: 1799px;\n\
            height: 570px;\n\
        }\n\
        .discribe{\n\
            display: inline;\n\
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