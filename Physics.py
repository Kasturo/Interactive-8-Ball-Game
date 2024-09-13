import phylib;

#a3 imports
import sqlite3;
import os;
from math import sqrt;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;


# add more here
# add the constants from phylib
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;  
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

#a3 constant
FRAME_RATE = 0.01;

#add provided  header
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="poolTable" width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

#add provided footer
FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        #create a fill color 
        fillColor = BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)];
        #return 
        #also have a cue ball case
        cueBall = False;
        if self.obj.still_ball.number == 0:
            cueBall = True;
        
        if cueBall == True:
            return f""" <circle id="cue-ball" cx = "{self.obj.still_ball.pos.x}" cy = "{self.obj.still_ball.pos.y}" r = "{BALL_RADIUS}" fill = "{fillColor}" />\n""";
        else:
            return f""" <circle id="still-ball" cx = "{self.obj.still_ball.pos.x}" cy = "{self.obj.still_ball.pos.y}" r = "{BALL_RADIUS}" fill = "{fillColor}" />\n""";

##ROllingBall
class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, pos, vel and acc as
        arguments.
        """
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_ROLLING_BALL, 
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0);
        
        self.__class__ = RollingBall;

    def svg(self):
        #seperately make fillColor
        fillColor = BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)];
        #define everything else in return line and return
        cueBall = False;
        if self.obj.rolling_ball.number == 0:
            cueBall = True;
        
        if cueBall == True:
            return f""" <circle id="cue-ball" cx = "{self.obj.rolling_ball.pos.x}" cy = "{self.obj.rolling_ball.pos.y}" r = "{BALL_RADIUS}" fill = "{fillColor}" />\n""";
        else:
            return f""" <circle id="rolling-ball" cx = "{self.obj.rolling_ball.pos.x}" cy = "{self.obj.rolling_ball.pos.y}" r = "{BALL_RADIUS}" fill = "{fillColor}" />\n""";




class Hole( phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires ball pos as arguments.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0);

        self.__class__ = Hole;
    
    def svg( self ):
        #return location rradius and fill color
        return f""" <circle cx="{self.obj.hole.pos.x}"  cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />\n""";


class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires ball y as arguments
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,
                                      None, None, None,
                                      0.0, y);

        self.__class__ = HCushion;
    def svg(self):
        #define value of y based off intstruction
        if self.obj.hcushion.y == 2700:
            y = 2700;
        else:
            y = -25;
        #return hcushion
        return f""" <rect width = "1400" height = "25" x="-25" y="{y}" fill = "darkgreen"/>\n""";

class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires ball x as arguments"""
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      None, None, None,
                                      x, 0.0);
        self.__class__ = VCushion;
    def svg(self):
        #defin x based off instruction
        if self.obj.vcushion.x == 0:
            x = -25;
        else:
            x = 1350; 
        #return vcushion     
        return f""" <rect width = "25" height = "2750" x="{x}" y="-25" fill = "darkgreen"/>\n""";

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        #initialize the return value with header
        svgReturn = HEADER;
        #loop through objects and if object exists add its svg to return
        for obj in self:
            if obj:
                svgReturn += obj.svg();
        #add footer to return
        svgReturn += FOOTER;
        #return
        return svgReturn;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number, Coordinate(0,0), Coordinate(0,0), Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
        
        if isinstance( ball, StillBall ):
            # create a new ball with the same number and pos as the old ball
            new_ball = StillBall( ball.obj.still_ball.number,
            Coordinate( ball.obj.still_ball.pos.x,
            ball.obj.still_ball.pos.y ) );
            # add ball to table
            new += new_ball;
        # return table
        return new;
    
    def initialTable(self):
        #localize variables for ease of use
        width = TABLE_WIDTH;
        length = TABLE_LENGTH;

        #set cue ball position
        cueBallX = width / 2.0;
        cueBallY = 3 * length / 4.0;
        
        #set center of table coordinates
        centerX = width / 2.0;
        centerY = length / 4.0;

        #set the space between the balls using diameter
        space = BALL_DIAMETER + 4.0;

        # create ball rack 
        rows = [
            [(0, 0)], # center ball
            [(-0.5, -sqrt(3)/2), (0.5, -sqrt(3)/2)], # two balls after 
            [(-1, -sqrt(3)), (0, -sqrt(3)), (1, -sqrt(3))], # 3 balls in third row
            [(-1.5, -sqrt(3)*1.5), (-0.5, -sqrt(3)*1.5), (0.5, -sqrt(3)*1.5), (1.5, -sqrt(3)*1.5)], #etc
            [(-2, -sqrt(3)*2), (-1, -sqrt(3)*2), (0, -sqrt(3)*2), (1, -sqrt(3)*2), (2, -sqrt(3)*2)]
        ]
        #initialize ballId at 1
        ballID = 1

        #initialize a row index
        row_index = 0

        # Loop until all rows are processed
        while row_index < len(rows):
            #get the current row
            row = rows[row_index]
            #initalize a positon index
            position_index = 0
            #loop until all balls
            while position_index < len(row):
                #get position from row
                (dx, dy) = row[position_index]
                #calculate the x and y pos
                pos_x = centerX + dx * space 
                pos_y = centerY + dy * space
                #create coordinate position
                position = Coordinate(pos_x, pos_y)
                #create still ball object
                still_ball = StillBall(ballID, position)
                #add ball to table
                self.add_object(still_ball)
                #increment ball id for next ball
                ballID += 1
                #move to next index
                position_index += 1
            #incrmeent rowIndex
            row_index += 1
        #create and add the cue ball object to the table
        cueBall = StillBall(0, Coordinate(cueBallX, cueBallY));
        self += cueBall;

        #create svg and return it
        svgContent = self.svg();
        return svgContent;

class Database:

    def __init__( self, reset=False ):
        #database filename
        db_filename = "phylib.db";

        #if reset is True, delete existing database file
        if reset and os.path.exists( db_filename ):
            os.remove( db_filename );

        #create or open database connection
        self.connection = sqlite3.connect( db_filename );
        self.cursor = self.connection.cursor();
        self.createDB();

    def createDB( self ):
        #create the necessary tables if they don't exist
        self.openConnection();

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO INTEGER,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT,
                YVEL FLOAT
        )
    """);
        
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS TTable(
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                TIME FLOAT NOT NULL
                            )
                            """);
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS BallTable(
                            BALLID INTEGER NOT NULL,
                            TABLEID INTEGER NOT NULL,
                            FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                            FOREIGN KEY (TABLEID) REFERENCES TTABLE(TABLEID)
        )""");
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Shot(
                            SHOTID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
                            PLAYERID INTEGER NOT NULL,
                            GAMEID INTEGER NOT NULL,
                            FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
                            FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
        )""");
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS TableShot(
                            TABLEID INTEGER NOT NULL,
                            SHOTID INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                            FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
        )""");
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Game(
                            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME VARCHAR(64) NOT NULL
        )""");
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Player(
                            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMEID INTEGER NOT NULL,
                            PLAYERNAME VARCHAR(64) NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES  Game(GAMEID)
        )""");

        #call close
        self.close();
    
    def readTable( self, tableID):
        #connect to db
        self.openConnection();

        #retrieve  ball information using tableID
        self.cursor.execute(''' 
            SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                            FROM Ball
                            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                            WHERE BallTable.TABLEID=?;
            ''', (tableID + 1,));
        ballData = self.cursor.fetchall();

        if not ballData:
            return None;

        #create table
        table = Table();
        #retreive the time for tableID 
        self.cursor.execute('''SELECT TIME FROM TTable WHERE TABLEID = ?''', (tableID + 1,)) ;
        time = self.cursor.fetchone()[0];
        table.time +=time;

        #loop through all of ball data
        for ballData in ballData:
            
            #store info from balldata into variables
            ball_id, ball_no, xpos, ypos, xvel, yvel = ballData

            #get coordinate position
            position = Coordinate(xpos,ypos);

            #rolling ballcase
            if xvel is not None and yvel is not None:
                velocity = Coordinate(float(xvel), float(yvel));
                xvelSqr = xvel * xvel;
                yvelSqr = yvel * yvel;
                speed = xvelSqr + yvelSqr;
                speed = sqrt(speed);
                if(speed > VEL_EPSILON):
                    accelX = (-xvel / speed) * DRAG;
                    accelY = (-yvel / speed) * DRAG;
                    acceleration = Coordinate(accelX, accelY);
                table += (RollingBall(ball_no, position, velocity, acceleration));
            #still ball case
            elif(xvel is None and yvel is None):
                table+= (StillBall(ball_no, position));
        #return the table created
        return table;

    def writeTable( self, table):
        #connect to db
        self.openConnection();

        #insert time into TTable
        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,));
        tableID = self.cursor.lastrowid;

        #loop through every ball in table
        for ball in table:
            #check if ball is rolling
            if isinstance(ball, RollingBall):
                #insert the rolling ball data into the table
                self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",(ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                ballID = self.cursor.lastrowid;
                #insert the ballid and tableid into balltable 
                self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballID, tableID));
            
            elif isinstance(ball, StillBall):
                #insert still ball into table
                self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)", (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y));
                ballID = self.cursor.lastrowid;
                #insert the ballid and tableid into balltable                 
                self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ballID, tableID));


        #close database
        self.close();
        #adjust and return table id
        return tableID -1;
    def openConnection(self):
        self.conn = sqlite3.connect("phylib.db");
        self.cursor = self.conn.cursor();
    
    def close(self):
        #check if exists then close
        if self.conn:
            self.conn.commit();        
        if self.cursor:
            self.cursor.close();
    
    def setGame( self, gameName, player1Name, player2Name):
        #connect database
        self.openConnection();

        #insert new row into Game table
        gameID = self.insertGame(gameName);

        gameID = self.cursor.lastrowid;   

        #insert player two rows for player
        self.insertPlayer(gameID, player1Name);
        self.insertPlayer(gameID, player2Name);


        #adjust gameId as needed
        gameID = gameID -1;

        #close database
        self.close();
        #return gameid
        return  gameID;
    
    def insertGame(self, gameName):
        #inserts row with gameName
        self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,));
        returnVal = self.cursor.lastrowid;

        #returns gameID
        return returnVal
    
    def insertPlayer(self, gameID, playerName):
        #insert the row into player table
        self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, playerName));
    
    def newShot(self, gameName, playerName):
        #connect database
        self.openConnection();
        #get gameID from game table with gamename
        self.cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,));
        #gameId var
        gameID = self.cursor.fetchone()[0];

        #get playerid same way from player table with playername
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?", (playerName, gameID));
        #get it in a var
        playerIDData = self.cursor.fetchone()[0];

        #insert row into shot table with both ids
        self.cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerIDData, gameID));
        #retreive shot id 
        shotID = self.cursor.lastrowid;
        #close database
        self.close();
        #adjust and return

        return shotID - 1;

    def addTable(self, tableId, shotID):
        self.openConnection();

        self.cursor.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableId, shotID,));

        self.close();



class Game():

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        #check for valid conditions
        if gameID is not None and (gameName is None or player1Name is not None or player2Name is not None):
            raise TypeError("invalid combination of arguments");

        #database connection
        db = Database();
        cursor = db.openConnection();
        
        
        #first constructor case
        if(gameID is not None):
            gameID += 1;
            #retreive values of gameName playerNames from the Game and Player tables
            cursor.execute("Select G.GAMENAME, P1.PLAYERNAME, P2.PLAYERNAME"
                        "FROM Game G"
                        "JOIN Player P1 ON G.GAMEID = P1.GAMEID "
                        "JOIN Player P2 ON G.GAMEID = P2.GAMEID "
                        "Where G.GAMEID = ?", (gameID,));
            data = cursor.fetchone();

            #set parameter values with retreived data
            self.gameID = data[0];
            self.gameName = data[1];
            self.player1Name = data[2];
            self.player2Name = data[3];
        #second constructor case
        elif(gameID is None and (gameName is not None and player1Name is not None and player2Name is not None)):
            #call on setgame method from database
            gameId = Database().setGame(gameName, player1Name, player2Name);

        #invalid case
        else:
            raise TypeError("invalid argument combinations");
        db.close();
    

    def shoot( self, gameName, playerName, table, xvel, yvel):
        #create databse
        db = Database();

        #step 1 add new entry and get shotID
        shotId = db.newShot(self, gameName, playerName);

        #step 2 find cue ball numebr 0
        # cue_Ball = db.cueBall();
        cue_Ball = table.cueBall();


        #step 3 retrieve x and y values of cue ball
        xpos = cue_Ball.obj.still_ball.pos.x;
        ypos = cue_Ball.obj.still_ball.pos.y;


        #step 5 set cue ball as rolling ball and set its associated values
        cue_Ball.type = phylib.PHYLIB_ROLLING_BALL;
        cue_Ball.obj.rolling_ball.pos.x = xpos;
        cue_Ball.obj.rolling_ball.pos.y = ypos;
        cue_Ball.obj.rolling_ball.vel.x = xvel;
        cue_Ball.obj.rolling_ball.vel.y = yvel;

        #step 6 clculate acceleration from a2 and a1
        #calulate accelration of rb
        ballSpeed = (xvel * xvel) + (yvel * yvel);
        ballSpeed = sqrt(ballSpeed);

        #do the thing from phylib bounce
        if ballSpeed > VEL_EPSILON:
            accelX = (-xvel / ballSpeed) * DRAG;
            accelY = (-yvel / ballSpeed) * DRAG;
        #final acceleration values set
        cue_Ball.obj.rolling_ball.acc.x = accelX;
        cue_Ball.obj.rolling_ball.acc.y = accelY;


        #step 7 set ball number 0
        cue_Ball.obj.rolling_ball.number = 0;   


        #step 8 loop over segment from a2 until retunr none
        #add first table 
        initialId = 0;
        db.addTable(initialId, shotId);

        #loop till table does not update
        while table:
            #update table by segment
            updatedTable = table.segment();

            #break condition
            if updatedTable is None:
                break;
            
            #calculate segement length 
            segmentLength = updatedTable.time - table.time;

            #calculate the iteration time
            iterateTime = int(segmentLength/FRAME_RATE);

            #loop the frame
            frameLoop(self, iterateTime, table, db, shotId);
            #update table
            table = updatedTable;
        #close database
        db.close();

def frameLoop(self, iterationTime, table, dataBase, shotID):

    #loop for iteration time
    for i in range(iterationTime):
        #calcualte time by framerate
        time = FRAME_RATE * i;
        #update current table information
        currTable = table.roll(time);
        currTable.time = table.time + time;
        currTableID = dataBase.writeTable(currTable);
        #add the current table to the database
        dataBase.addTable(currTableID, shotID);




        

        
