#bmpが入っているディレクトリで実行してください
import glob
def main():
    paths = glob.glob("./*bmp")
    part1 = '<!DOCTYPE html>\n\
    <html>\n\
    <head>\n\
        <title>viewer</title>\n\
    </head>\n\
    <body>\n\
        <p id="currentpath"></p>\n\
        <img id="output" src=""><br><br>\n\
        <div class="navi">\n\
            <input type="button" value="100戻る" onclick="move(-100);"/>\n\
            <input type="button" value="10戻る" onclick="move(-10);"/>\n\
            <input type="button" value="1戻る" onclick="move(-1);"/>\n\
            <input type="button" value="1進む" onclick="move(1);"/>\n\
            <input type="button" value="10進む" onclick="move(10);"/>\n\
            <input type="button" value="100進む" onclick="move(100);"/>\n\
        </div>\n\
        <br/>\n\
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
    \n\
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
      </style>'

    for p in paths:
        part1 += f"'{p}',\n"
    all = part1+part2
    with open("viewer.html", "w") as f:
        f.write(all)

if __name__ == '__main__':
    main()