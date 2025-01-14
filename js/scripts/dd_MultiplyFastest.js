// dd_MultiplyFastest.js
// Multiply fastest moving mv's
var LARGEST = 0;

// global variable holding forward motion vectors from previous frames
var prev_fwd_mvs = [ ];

/**
 * @param {number} percent - The percentage of fastest mvs to multiply
 * @param {number} multiple - The amount to multiply by
 */
export function glitch_frame(frame, percent = 50, multiple = 10)
{
    var percentage = percent / 100
	LARGEST = 0;
    // bail out if we have no motion vectors
    let mvs = frame["mv"];
    if ( !mvs )
        return;
    // bail out if we have no forward motion vectors
    let fwd_mvs = mvs["forward"];
    if ( !fwd_mvs )
        return;

   	// 1st loop - find the fastest mv
   	// this ends-up in LARGEST as the square of the hypotenuse (mv[0]*mv[0]) + (mv[1]*mv[1])
    let W = fwd_mvs.length;
    for ( let i = 0; i < fwd_mvs.length; i++ )
    {
        let row = fwd_mvs[i];
        // rows
        let H = row.length;
        for ( let j = 0; j < row.length; j++ )
        {
            // loop through all macroblocks
            let mv = row[j];

            // THIS IS WHERE THE MEASUREMENT HAPPENS
            var this_mv = (mv[0] * mv[0])+(mv[1] * mv[1]);
            if ( this_mv > LARGEST){
				LARGEST = this_mv;
			}
        }
    }

    // then find those mv's which are bigger than SOME_PERCENTAGE of LARGEST
    // and then replace them with the average mv from the last n frames
    for ( let i = 0; i < fwd_mvs.length; i++ )
	    {
	        let row = fwd_mvs[i];
	        // rows
	        let H = row.length;
	        for ( let j = 0; j < row.length; j++ )
	        {
	            // loop through all macroblocks
	            let mv = row[j];

	            // THIS IS WHERE THE MAGIC HAPPENS
	            var this_mv = (mv[0] * mv[0])+(mv[1] * mv[1]);
	            if (this_mv > (LARGEST * percentage)){

			     	mv[0] = mv[0] * multiple;
					mv[1] = mv[1] * multiple;
				}
	        }
    }
}
