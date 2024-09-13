#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "phylib.h"

//Part 1
phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos ){
    if (pos == NULL)
    {
        return NULL; //error case
    }
    
    phylib_object *newObject = malloc(sizeof(phylib_object)); //do I cast this???

    //allocation fail
    if (newObject == NULL)
    {
        return NULL;
    }

    //set object parameters and type
    newObject->type = PHYLIB_STILL_BALL;
    newObject->obj.still_ball.number = number;
    newObject->obj.still_ball.pos = *pos;

    //return object
    return newObject;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    if (pos == NULL || vel == NULL || acc == NULL)
    {
        return NULL; //errror case
    }
    
    //malloc object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    //allocation fail
    if (newObject == NULL)
    {
        return NULL;
    }

    //set type and object parameters
    newObject->type = PHYLIB_ROLLING_BALL;
    newObject->obj.rolling_ball.number = number;
    newObject->obj.rolling_ball.pos = *pos;
    newObject->obj.rolling_ball.vel = *vel;
    newObject->obj.rolling_ball.acc = *acc;

    //return object
    return newObject;
}

phylib_object *phylib_new_hole( phylib_coord *pos ){
    if (pos == NULL)
    {
        return NULL;//error case
    }
    
    //new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    //allocation fail
    if (newObject == NULL)
    {
        return NULL;
    }

    //set type and param
    newObject->type = PHYLIB_HOLE;
    newObject->obj.hole.pos = *pos;

    //rreturn
    return newObject;
    
}

phylib_object *phylib_new_hcushion( double y ){
    //new object
    phylib_object *newObject = malloc(sizeof(phylib_object));
    //allocation fail
   if (newObject == NULL)
    {
        return NULL;
    }
    //set param and type
    newObject->type = PHYLIB_HCUSHION;
    newObject->obj.hcushion.y = y;
    //return
    return newObject;
}

phylib_object *phylib_new_vcushion( double x ){
    //new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    //allocation fail
   if (newObject == NULL)
    {
        return NULL;
    }

    //set param and type
    newObject->type = PHYLIB_VCUSHION;
    newObject->obj.vcushion.x = x;

    //return
    return newObject;
}

phylib_table *phylib_new_table( void ){
    //new table
    phylib_table *newTable = malloc(sizeof(phylib_table));
    //allocation fail
    if (newTable == NULL)
    {
        return NULL;
    }

    //set every object to NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        newTable->object[i] = NULL;
    }

    //set time to 0
    newTable->time = 0.0;

    //NOTE: width = length/2

    //set all table objects
    //cushions
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //holes
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});
    
    //return tabkle
    return newTable;
}


//Part 2
void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    //if src null then make dest null
    if (*src == NULL)
    {
        *dest = NULL;
    }
    else{
        //allocate the memory for a new phylib_object
        *dest = malloc(sizeof(phylib_object));
        //allocation fail
        if (*dest == NULL)
        {
            return;
        }
        //copy mem from soruce to destination
        memcpy(*dest, *src, sizeof(phylib_object));
        
    }
}

phylib_table *phylib_copy_table( phylib_table *table ){
    //og table dont exist error trap
    if (table == NULL)
    {
        return NULL;
    }
    
    //allocate new table
    phylib_table *newTable = malloc(sizeof(phylib_table));
    //allocation fail
    if (newTable == NULL)
    {
        return NULL;
    }

    //copy table memory from og to new
    memcpy(newTable, table, sizeof(phylib_table));

    //copy each individual object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
        }   
    }
    //return table
    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ){
    if (table == NULL || object == NULL)
    {
        return; // error case
    }
    

    //loop throuhg each object until NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {   
        //add object at NULL
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }  
    }
}

void phylib_free_table( phylib_table *table ){
    if (table == NULL)
    {
        return; //table is empty
    }

    //loop through each object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {   
        //if not NULL, free
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }
    //free entire table
    free(table);    
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    //initialize variables
    phylib_coord newCord;

    //perform subtraction operation on x and y
    newCord.x = c1.x - c2.x;
    newCord.y = c1.y - c2.y;
    //return new coordintae
    return newCord;
}

double phylib_length( phylib_coord c ){
    //intilaize variable
    double length;

    //perform pythagorean 
    length = (c.x * c.x) + (c.y*c.y);
    //finish pythagorean and return
    return sqrt(length);
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){
    //intialize variable
    double dotProd;
    //perform dot product operation
    dotProd = (a.x * b.x) + (a.y*b.y);

    //return dotprroduct
    return dotProd;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    //NULL case error trap
    if (obj1 == NULL || obj2 == NULL)
    {
        return -1;
    }
    
    //check if type does not match
    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }

    //intialize variables
    phylib_coord position1 = obj1->obj.rolling_ball.pos;
    phylib_coord position2;
    double finalPosition;

    //switch cases for different object types
    switch (obj2->type)
    {
    //still ball and rolling ball are done in same case
    case PHYLIB_ROLLING_BALL:
    case PHYLIB_STILL_BALL:
        //set position for rolling
        if(obj2->type == PHYLIB_ROLLING_BALL){
            position2 = obj2->obj.rolling_ball.pos;
        }
        //for still
        else{
            position2 = obj2->obj.still_ball.pos;
        }
        //calculate distance
        finalPosition = phylib_length(phylib_sub(position1, position2)) - PHYLIB_BALL_DIAMETER;
        break;
    case PHYLIB_HOLE:
        //set pos
        position2 = obj2->obj.hole.pos;
        //calculate distance
        finalPosition = phylib_length(phylib_sub(position1,position2)) - PHYLIB_HOLE_RADIUS;
        break;
    case PHYLIB_HCUSHION:
        //calculate distance
        finalPosition = fabs(position1.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
        break;
    case PHYLIB_VCUSHION:
        //calcualte distance
        finalPosition = fabs(position1.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
        break;
    default:   
        //error case
        return -1;
        break;
    }

    //return
    return finalPosition;
    
}


//part 3
void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    //error case cehck
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    //calculate new position
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + ((0.5) * old->obj.rolling_ball.acc.x * (time*time));
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + ((0.5) * old->obj.rolling_ball.acc.y * (time*time));

    //calculate vel
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    //see if either x or y change sign
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0)
    {
        new->obj.rolling_ball.acc.x = 0;
        new->obj.rolling_ball.vel.x = 0;
    }
    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0)
    {
        new->obj.rolling_ball.acc.y = 0;
        new->obj.rolling_ball.vel.y = 0;
    }
}

unsigned char phylib_stopped( phylib_object *object ){
    //check if length is less than eppsilon 
    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON)
    {
        //set type to still and return 1
        object->type = PHYLIB_STILL_BALL;

        return 1;
    }
    //ntohing done return 0
    return 0;
    
}

void phylib_bounce( phylib_object **a, phylib_object **b ){

    //intialize var
    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    double aSpeed;
    double bSpeed;
    double v_rel_n;

    //cases for b type
    switch ((*b)->type)
    {
    // horizontal cushion, change direction on y
    case PHYLIB_HCUSHION:
        (*a)->obj.rolling_ball.vel.y *= -1;
        (*a)->obj.rolling_ball.acc.y *= -1;
        break;
    //vertical cushion, change direction on x
    case PHYLIB_VCUSHION:
        (*a)->obj.rolling_ball.vel.x *= -1;
        (*a)->obj.rolling_ball.acc.x *= -1;
        break;
    //hole, bye bye ball
    case PHYLIB_HOLE:
        free((*a));
        (*a) = NULL;
        break;
    //still ball
    case PHYLIB_STILL_BALL:
        //set still ball to moving
        (*b)->type = PHYLIB_ROLLING_BALL;
        //make sure posiition and ball number all match up after switch
        (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
        (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
        (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;       
        //makesure balls acc and vel are intialized to 0
        (*b)->obj.rolling_ball.acc = (phylib_coord){0.0,0.0};
        (*b)->obj.rolling_ball.vel = (phylib_coord){0.0,0.0};
    //rolling ball
    case PHYLIB_ROLLING_BALL:
        //calculate r_ab and v_rel
        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
        //if 0, set all x and y to 0 cause /0 not possible
        if (phylib_length(r_ab) == 0)
        {
            n.x = 0;
            n.y = 0;
        }
        else
        {
            //calculate n
            n.x = (r_ab.x) / (phylib_length(r_ab));
            n.y = (r_ab.y) / (phylib_length(r_ab));
        }
        

        //velocity relative to n calculation
        v_rel_n = phylib_dot_product(v_rel, n);

        //update a and b
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

        (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

        //calculate a Speed and b Speed
        aSpeed = phylib_length((*a)->obj.rolling_ball.vel);
        bSpeed = phylib_length((*b)->obj.rolling_ball.vel);
        //make sure acceleration correct? idk what this does tbh, I just followed the instructions
        if (aSpeed > PHYLIB_VEL_EPSILON) {
            (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / aSpeed) * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / aSpeed) * PHYLIB_DRAG;
        }
        if (bSpeed > PHYLIB_VEL_EPSILON) {
            (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / bSpeed) * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / bSpeed) * PHYLIB_DRAG;
        }        
        break;
    default:
        //not a valid type case
        break;
    }
}

unsigned char phylib_rolling( phylib_table *t ) {
    if (t == NULL)
    {
        return -1; //table empty
    }
    
    //set count at 0
    unsigned char count = 0;

    //loop throuhg all objects 
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        //if not NULL and is ROLLING
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            //counter increment
            count++;
        }
    }
    //return num of rolling ballz
    return count; 
}

phylib_table *phylib_segment( phylib_table *table ){
    //make sure table is not null and balls are rolling
    if (table == NULL|| phylib_rolling(table) == 0)
    {
        //error case
        return NULL;
    }

    //create copy tbale
    phylib_table *copyTable = phylib_copy_table(table);

 
    
    //iterate overr time
    for (double time = PHYLIB_SIM_RATE; time <= PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE)
    {
        // //loop over all objects
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
        {   
            //if not NULL and type is rolling ball
            if (copyTable->object[j] != NULL && copyTable->object[j]->type == PHYLIB_ROLLING_BALL)
            {
                //call roll
                phylib_roll(copyTable->object[j], table->object[j], time);

                //if stopped check add time and return table
                if (phylib_stopped(copyTable->object[j]))
                {
                    copyTable->time += time;
                    return copyTable;
                }
            }
        }

        //check colisions
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
        {   
            //if rolling and not NULL
            if (copyTable->object[j] != NULL && copyTable->object[j]->type == PHYLIB_ROLLING_BALL)
            {
                //loop through all objects
                for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++)
                {
                    //make sure we not comparing same object and make sure object k isnt null
                    if (j != k && copyTable->object[k] != NULL)
                    {
                        //if distance between two objects is less than 0 
                        if (phylib_distance(copyTable->object[j], copyTable->object[k]) < 0.0)
                        {
                            //call boucn and record time and return copy
                            phylib_bounce(&copyTable->object[j], &copyTable->object[k]);
                            copyTable->time += time;
                            return copyTable;
                        }
                    }
                }
            }
        }
    }
    
    //return copy 
    return copyTable;

}


//A2 function
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf( string, 80, "STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf( string, 80, "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
        object->obj.rolling_ball.number,
        object->obj.rolling_ball.pos.x,
        object->obj.rolling_ball.pos.y,
        object->obj.rolling_ball.vel.x,
        object->obj.rolling_ball.vel.y,
        object->obj.rolling_ball.acc.x,
        object->obj.rolling_ball.acc.y );
        break;
    case PHYLIB_HOLE:
        snprintf( string, 80, "HOLE (%6.1lf,%6.1lf)",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
        break;
    case PHYLIB_HCUSHION:
        snprintf( string, 80, "HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
        break;
    case PHYLIB_VCUSHION:
        snprintf( string, 80, "VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
    }
    return string;
}
