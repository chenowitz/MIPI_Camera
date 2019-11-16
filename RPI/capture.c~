#include "arducam_mipicamera.h"
#include <linux/v4l2-controls.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define LOG(fmt, args...) fprintf(stderr, fmt "\n", ##args)

#define FOCUS_VAL  270  //range(0-65535)

#define SOFTWARE_AE_AWB
                   //IMAGE_ENCODING_JPEG
                   //IMAGE_ENCODING_BMP
                   //IMAGE_ENCODING_PNG
IMAGE_FORMAT fmt = {IMAGE_ENCODING_JPEG, 50};

typedef struct
{
   int id;
   char *command;
   char *abbrev;
   char *help;
   int num_parameters;
} COMMAND_LIST;

enum
{
   CommandTimeout,
   CommandQuality,
   CommandMode,
   CommandAutowhitebalance,
   CommandAutoexposure,
   //CommandHelp,
   CommandFocus,
   CommandRedVal,
   CommandBlueVal, 
   
};

static COMMAND_LIST cmdline_commands[] =
{
   { CommandTimeout, "-timeout",    "t",  "Time (in ms) before takes picture and shuts down (if not specified, loop)", 1 },
   { CommandQuality, "-quality",    "q",  "Set jpeg quality <0 to 100>", 1 },
   { CommandMode, "-mode",    "m",    "Set sensor mode", 1},
   { CommandAutowhitebalance, "-autowhitebalance",    "awb",    "Enable or disable awb", 1 },

   { CommandAutoexposure, "-autoexposure",    "ae",    "Enable or disable ae", 1 },

   //{ CommandHelp, "-help",    "?",    "This help information", 0},
   { CommandFocus, "-focus", "f", "Set focus value of camera", 1 },
   { CommandRedVal, "-red_bal", "rb", "Set red balance value", 1 },
   { CommandBlueVal, "-blue_bal", "bb", "Set blue balance value", 1 },

};

typedef struct
{
   int timeout;                        // Time taken before frame is grabbed and app then shuts down. Units are milliseconds
   int quality;                        // JPEG quality setting (1-100)
   int mode;                           // sensor mode
   int awb_state;                      // auto white balance state
   int ae_state;                       // auto exposure state
   int focus; 					            // focus state 
   int red_bal; 								// red balance 
   int blue_bal;								// blue balance

} RASPISTILL_STATE;


static int arducam_parse_cmdline(int argc, char **argv, RASPISTILL_STATE *state);
int raspicli_get_command_id(const COMMAND_LIST *commands, const int num_commands, const char *arg, int *num_parameters);
static int cmdline_commands_size = sizeof(cmdline_commands) / sizeof(cmdline_commands[0]);
static void default_status(RASPISTILL_STATE *state);
//void raspicli_display_help(const COMMAND_LIST *commands, const int num_commands);
//void raspipreview_display_help();
//void printCurrentMode(CAMERA_INSTANCE camera_instance);


void save_image(CAMERA_INSTANCE camera_instance, const char *name) {
	RASPISTILL_STATE state; //does the declaration of 'state' here mess anything up?  
    // The actual width and height of the IMAGE_ENCODING_RAW_BAYER format and the IMAGE_ENCODING_I420 format are aligned, 
    // width 32 bytes aligned, and height 16 byte aligned.
    //LOG("Setting the focus to the command line entry...");
    	//printf("Please enter focus:");
	//int focus = (int)(getchar()-'0');
        //if (arducam_set_control(camera_instance, V4L2_CID_FOCUS_ABSOLUTE,state.focus)) {
            //LOG("Failed to set focus, the camera may not support this control.");
        //} 
        
        
        //usleep(1000 * 1000 * 2);
    /*LOG("Enable Manual Red Balance...");
    if (arducam_set_control(camera_instance, V4L2_CID_RED_BALANCE,state.red_bal)) { //*********************************
        LOG("Failed to set desired focus value, the camera may not support this control.");
    } 
    
    
	 //usleep(1000 * 1000 * 2);    
    LOG("Enable Manual Blue Balance...");
    if (arducam_set_control(camera_instance, V4L2_CID_BLUE_BALANCE,state.blue_bal)) { //*********************************
       LOG("Failed to set desired focus value, the camera may not support this control.");
    }   
    
    //usleep(1000 * 1000 * 2);
    LOG("Enable Gains...");
    arducam_manual_set_awb_compensation(0xFFFFFFFE,0);*/
        
        
        
#if defined(SOFTWARE_AE_AWB)
    LOG("Enable Software Auto Exposure...");
    arducam_software_auto_exposure(camera_instance, 1);
    LOG("Enable Software Auto White Balance...");
    arducam_software_auto_white_balance(camera_instance, 1);
   LOG("Waiting for automatic adjustment to complete...");
    usleep(1000 * 1000 * 1);
#endif
        usleep(1000*10);
    BUFFER *buffer = arducam_capture(camera_instance, &fmt, 12000);
    if (!buffer) {
        LOG("capture timeout.");
        return;
    }
    FILE *file = fopen(name, "wb");
    fwrite(buffer->data, buffer->length, 1, file);
    fclose(file);
    arducam_release_buffer(buffer);
}

int main(int argc, char **argv) {
   CAMERA_INSTANCE camera_instance;
	RASPISTILL_STATE state;
  	default_status(&state);
  	if (arducam_parse_cmdline(argc, argv, &state))
   {
     return 0;
   }     
    
    int width = 0, height = 0;
    char file_name[100];

    LOG("Open camera...");
    int res = arducam_init_camera(&camera_instance);
    if (res) {
        LOG("init camera status = %d", res);
        return -1;
    }

    struct format support_fmt;
    int index = 0;
    char fourcc[5];
    fourcc[4] = '\0';
    while (!arducam_get_support_formats(camera_instance, &support_fmt, index++)) {
        strncpy(fourcc, (char *)&support_fmt.pixelformat, 4);
        LOG("mode: %d, width: %d, height: %d, pixelformat: %s, desc: %s", 
            support_fmt.mode, support_fmt.width, support_fmt.height, fourcc, 
            support_fmt.description);
    }
    index = 0;
    struct camera_ctrl support_cam_ctrl;
    while (!arducam_get_support_controls(camera_instance, &support_cam_ctrl, index++)) {
        int value = 0;
        if (arducam_get_control(camera_instance, support_cam_ctrl.id, &value)) {
            LOG("Get ctrl %s fail.", support_cam_ctrl.desc);
        }
        LOG("index: %d, CID: 0x%08X, desc: %s, min: %d, max: %d, default: %d, current: %d",
            index - 1, support_cam_ctrl.id, support_cam_ctrl.desc, support_cam_ctrl.min_value,
            support_cam_ctrl.max_value, support_cam_ctrl.default_value, value);
    }
    LOG("Focus set in main loop");
        if (arducam_set_control(camera_instance, V4L2_CID_FOCUS_ABSOLUTE,state.focus)) {
            LOG("Failed to set focus, the camera may not support this control.");
        } 
    //printf("Please enter focus value:");
    //int focus = (int)(getchar()-'0');
    //res= arducam_set_control(camera_instance,V4L2_CID_FOCUS_ABSOLUTE,focus);
    
    //if(res){
	//LOG("Something went wrong");    
    	//return -1;
    //}else{
    	//printf("Setting the focus...");    
    //}

    printf("Please choose sensor mode: ");
    int mode = 3;//(int)(getchar()-'0');
    //arducam_set_control(camera_instance,V4L2_CID_FOCUS_ABSOLUTE,focus);
    //printf("Setting the focus...");
    //printf("Please choose sensor mode: ");
    LOG("Setting the mode...");
   // res = arducam_set_resolution(camera_instance, &width, &height);
    printf("choose the mode %d\r\n", mode );
    res= arducam_set_mode(camera_instance, mode);
    if (res) {
        LOG("set resolution status = %d", res);
        return -1;
    } else {
        LOG("Current mode  is %d", mode);
        LOG("Notice:You can use the list_format sample program to see the resolution and control supported by the camera.");
    }

    //printf("Please enter focus value:");
    //int focus = (int)(getchar()-'0');
    //arducam_set_control(camera_instance,V4L2_CID_FOCUS_ABSOLUTE,focus);
   // printf("Setting the focus...");
   
   
	 //usleep(1000 * 1000 * 2);
    LOG("Enable Manual Red Balance...");
    if (arducam_set_control(camera_instance, V4L2_CID_RED_BALANCE,state.red_bal)) { //*********************************
        LOG("Failed to set desired focus value, the camera may not support this control.");
    } 
    
    
	 //usleep(1000 * 1000 * 2);    
    LOG("Enable Manual Blue Balance...");
    if (arducam_set_control(camera_instance, V4L2_CID_BLUE_BALANCE,state.blue_bal)) { //*********************************
       LOG("Failed to set desired focus value, the camera may not support this control.");
    }   
    
    //usleep(1000 * 1000 * 2);
    LOG("Enable Gains...");
    arducam_manual_set_awb_compensation(0xFFFFFFFE,0);
   
   

    if(fmt.encoding == IMAGE_ENCODING_JPEG){
        sprintf(file_name, "mode%d.jpg", mode);
    }
    if(fmt.encoding == IMAGE_ENCODING_BMP){
        sprintf(file_name, "mode%d.bmp", mode);
    }
    if(fmt.encoding == IMAGE_ENCODING_PNG){
        sprintf(file_name, "mode%d.png", mode);
    } 
    LOG("Capture image %s...", file_name);
    save_image(camera_instance, file_name);

    LOG("Close camera...");
    res = arducam_close_camera(camera_instance);
    if (res) {
        LOG("close camera status = %d", res);
    }
    return 0;
}


int raspicli_get_command_id(const COMMAND_LIST *commands, const int num_commands, const char *arg, int *num_parameters)
{
   int command_id = -1;
   int j;

   if (!commands || !num_parameters || !arg)
      return -1;


   for (j = 0; j < num_commands; j++)
   {
      if (!strcmp(arg, commands[j].command) ||
            !strcmp(arg, commands[j].abbrev))
      {
         // match
         command_id = commands[j].id;
         *num_parameters = commands[j].num_parameters;
         break;
      }
   }

   return command_id;
}


static int arducam_parse_cmdline(int argc, char **argv,RASPISTILL_STATE *state){
    int valid =1;
    int i ;
    for (i=1; i< argc && valid; i++){
        int command_id, num_parameters;
        if( !argv[i])
            continue;
        if(argv[i][0] != '-')
        {
            valid =0;
            continue;
        }
        valid = 1;
        command_id =raspicli_get_command_id(cmdline_commands, cmdline_commands_size, &argv[i][1], &num_parameters);
        //if(command_id == CommandHelp){
             //raspipreview_display_help(); valid = 0;
        //}
        // If we found a command but are missing a parameter, continue (and we will drop out of the loop)
        if (command_id != -1 && num_parameters > 0 && (i + 1 >= argc) )
         continue;
        switch (command_id)
        {
        case CommandMode:
              {
                if (sscanf(argv[i + 1], "%d", &state->mode) == 1)
                 {
                    //printf("state->mode = %d\r\n",state->mode);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } 
            case CommandTimeout:
              {
                 if (sscanf(argv[i + 1], "%d", &state->timeout) == 1)
                 {
                    i++;
                   // printf("state->timeout = %d\r\n", state->timeout);
                 }
                 else
                    valid = 0;
                 break;
              }
            case CommandQuality:
              {
                if (sscanf(argv[i + 1], "%u", &state->quality) == 1)
                 {
                    if (state->quality > 100)
                    {
                       fprintf(stderr, "Setting max quality = 100\n");
                       state->quality = 100;
                    }
                    i++;
                 }
                else
                    valid = 0;
                break;
              }
             case CommandAutowhitebalance:
              {
                if (sscanf(argv[i + 1], "%d", &state->awb_state) == 1)
                 {
                 //   printf("state->awb_state = %d\r\n",state->awb_state);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } 
             case CommandAutoexposure:
              {
                if (sscanf(argv[i + 1], "%d", &state->ae_state) == 1)
                 {
                  //  printf("state->ae_state = %d\r\n",state->ae_state);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } 
             case CommandFocus: //*********************************
              {
                if (sscanf(argv[i + 1], "%d", &state->focus) == 1)
                 {
                  //  printf("state->ae_state = %d\r\n",state->ae_state);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } //*********************************
				case CommandRedVal: //*********************************
              {
                if (sscanf(argv[i + 1], "%d", &state->red_bal) == 1)
                 {
                  //  printf("state->ae_state = %d\r\n",state->ae_state);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } //*********************************
             case CommandBlueVal: //*********************************
              {
                if (sscanf(argv[i + 1], "%d", &state->blue_bal) == 1)
                 {
                  //  printf("state->ae_state = %d\r\n",state->ae_state);
                    i++;
                 }
                else
                    valid = 0;
                break;
              } //*********************************
            
        }
    }

   if (!valid)
   {
      //fprintf(stderr, "Invalid command line option (%s)\n", argv[i-1]);
      return 1;
   }
   return 0;
}


static void default_status(RASPISTILL_STATE *state)
{
    state->mode = 0;
    state->ae_state =1;
    state->awb_state = 1;
    state->quality = 50;
    state->timeout = 5000;
    state->focus = 65535; //*********************************
    state->red_bal = 2000;
    state->blue_bal = 3000; 
}
