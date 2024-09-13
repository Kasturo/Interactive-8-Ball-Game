#export LD_LIBRARY_PATH=`pwd` 

import sys
import cgi
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import Physics
from math import sqrt
import glob

class MyHandler(BaseHTTPRequestHandler):
    #create table and database 
    table = Physics.Table();
    dataB = Physics.Database(reset=True);
    #declare the varibales for game, playername and playerturn
    game = None
    player1Name = None;
    player2Name = None;
    playerTurn = None;

    #doGet
    def do_GET(self):
        parsed = urlparse(self.path);
        #check web pages match
        if parsed.path in [ '/shoot.html' ]:
            #check for path
            if os.path.exists('./shoot.html'):
                with open('./shoot.html' , 'rb') as file:
                    content = file.read();
                #generate headers
                self.send_response(200);
                self.send_header( "Content-type", "text/html" );
                self.send_header( "Content-length", len( content ) );
                self.end_headers();           
                #send info to browser
                self.wfile.write(content);
            #exception case of when path doesnt not exist
            else:
                self.send_error(404,'File Not Found!');
        #check path for menu
        elif parsed.path == "/menuPage.html":
            if os.path.exists('./menuPage.html'):
                with open('./menuPage.html', 'rb') as file:
                    content = file.read();
                #send responses for content of menupage
                self.send_response(200);
                self.send_header("Content-type", "text/html");
                self.send_header("Content-length", len(content));
                self.end_headers();
                self.wfile.write(content);
            #error case 404
            else:
                self.send_error(404, 'File Not Found!');
        
        #check for the initial table 
        elif parsed.path == "/init_table":
            #send the response for the webpage
            self.send_response(200);
            self.send_header('Content-type', 'image/svg+xml');
            self.end_headers();
            #generate the initial table 
            svgCont = MyHandler.table.initialTable();

            self.wfile.write(svgCont.encode('utf-8'));
        #error
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: $s not found" % self.path, "utf-8"));     
     
    #do_POST
    def do_POST(self):
        #parse url
        parsed = urlparse(self.path);
        
        #check path is in display
        if parsed.path in ['/display.html']:
            #get data as multiparrt formData
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"]}
            )
            
            #delete exisitng table svg
            for svgFile in glob.glob("./table-*.svg"):
                os.remove(svgFile);
            #step 3
            #set up still ball info
            sbNum = int(form.getvalue('sb_number'));
            stillBall_x = float(form.getvalue('sb_x'));
            stillBall_y = float(form.getvalue('sb_y'));
            sbPos = Physics.Coordinate(stillBall_x, stillBall_y);



            #roling ball information
            rbNum = int(form.getvalue('rb_number'));
            rollBall_x = float(form.getvalue('rb_x'));
            rollBall_y = float(form.getvalue('rb_y'));


            #rolling ball vel
            rbVel_x = float(form.getvalue('rb_dx'));
            rbVel_y = float(form.getvalue('rb_dy'));


            #calculate the position and velocity of rolling ball
            rbPos = Physics.Coordinate(rollBall_x, rollBall_y);
            rbVel = Physics.Coordinate(rbVel_x, rbVel_y);

            #calculate acceleration of a rolling ball
            velXSqr = (rbVel_x * rbVel_x);
            velYSqr = (rbVel_y * rbVel_y);
            ballSpeed = (velXSqr) + (velYSqr)
            ballSpeed = sqrt(ballSpeed);

            #do the thing from bounch in phylib
            if ballSpeed > Physics.VEL_EPSILON:
                rbAccX = (-rbVel_x / ballSpeed) * Physics.DRAG;
                rbAccY = (-rbVel_y / ballSpeed) * Physics.DRAG;
            #final rolling ball acceleration
            rbAcc = Physics.Coordinate(rbAccX, rbAccY);

            #step 4
            #initilaize test table
            testTable = Physics.Table();
            #init still ball and rolling ball
            stillBall = Physics.StillBall(sbNum, sbPos);
            rollBall = Physics.RollingBall(rbNum, rbPos, rbVel, rbAcc);
            #add both to table
            testTable += stillBall;
            testTable += rollBall;
            

            #step 5
            #create loop index
            indexCounter = 0;
    

            #loop through table
            while testTable: 
                #open svg path as file
                with open(f"table-{indexCounter}.svg", "w") as file:
                    svgInfo = testTable.svg();
                    #rwite th svg content to files
                    file.write(svgInfo);
                testTable = testTable.segment();
                #incrmeent loop
                indexCounter+=1;
            
            #initialize a svgFiles list
            svgFiles = [];
            
            #get all svg files
            for file in os.listdir():
                #makes sure we are getting a svg file
                if file.startswith('table-') and file.endswith('.svg'):
                    svgFiles.append(file);
            
            #set up web page content
            htmlWPContent = '<h1>Information Display Page:<h1>';
            #add svg to WP content
            for svgFile in  svgFiles:
                htmlWPContent+= f'<img src="{svgFile}" alt="Table Image">\n';
            #step 6
            #add information of still ball, rolling ball pos, and rolling ball position
            htmlWPContent += f'<h3>Still Ball Position:({stillBall_x}, {stillBall_y})</h3>\n'
            htmlWPContent += f'<h3>Rolling Ball Position:({rollBall_x}, {rollBall_y})</h3>\n'
            htmlWPContent += f'<h3>Rolling Ball Velocity:({rbVel_x}, {rbVel_y})</h3>\n'
            #create a return button
            htmlWPContent += '\n<button onclick="window.location.href=\'/shoot.html\'">Back</button>\n'

            #step 7?
            #send repsonse of 200 back
            self.send_response(200);
            self.send_header('content-type', 'text/html');
            self.end_headers();
            self.wfile.write(bytes(htmlWPContent,"utf-8"));
        
        elif parsed.path == "/submit_menu":
            #parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"]}
            )
            
            #get the playernames from the post data
            player1_name = form.getvalue('player1name', '')
            player2_name = form.getvalue('player2name', '')

            #now store those local variables into the global
            self.player1Name = player1_name
            self.player2Name = player2_name

            #create the game object not
            self.game = Physics.Game(gameName="game01", player1Name=self.player1Name, player2Name=self.player2Name);

            #after player submits have them redirected to a page
            self.send_response(302)  #redirect status for temporary redirection
            #after the temporary redirection ahve them sent to shoot.html with playernames sent as well
            self.send_header('Location', f'/shoot.html?player1name={player1_name}&player2name={player2_name}')
            self.end_headers()

        
        


if __name__ == "__main__":
    #ensure the arguments exist
    if len(sys.argv) < 2:
        print("Usage Python server.py <port>");
        sys.exit(1);
    #extract port from command line
    port = int(sys.argv[1]);
    #lab serrver stuff
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
