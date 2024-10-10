import { SCRIPTS } from "./ScriptDatabseBackup.js";
import data from './GlitchSequence.js'; 

var FRAME_COUNTER = 0;

var glitchList = data;

export function setup(){
    for (var i = 0; i < glitchList.length; i++) {
        glitchList[i].func = SCRIPTS[glitchList[i].name]
    }
}

export function glitch_frame(frame){
    // Increment Frame Count
    FRAME_COUNTER++;
    
    // Based on frame count, apply array of glitches
    for (var g = 0; g < glitchList.length; g++ ){
        var glitch = glitchList[g]
        if (FRAME_COUNTER >= glitch.start && FRAME_COUNTER <= glitch.end){
            var params = glitch.params;

            print(`Applying Glitch ${glitch.name} with params: ${params} to frame ${FRAME_COUNTER}`)

            glitch.func(frame, params[0], params[1], params[2])
        }
    }
}