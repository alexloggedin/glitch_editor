// dd_zoom_out.js

/**
 * @param {number} zoomVal - The value to zool out by
 */
export function glitch_frame(frame, zoomVal = 20)
{
    var zoom = -1 * zoomVal
    // bail out if we have no motion vectors
    let mvs = frame["mv"];
    if ( !mvs )
        return;
    // bail out if we have no forward motion vectors
    let fwd_mvs = mvs["forward"];
    if ( !fwd_mvs )
        return;

	var M_H = fwd_mvs.length/2;
    // clear horizontal element of all motion vectors
    for ( let i = 0; i < fwd_mvs.length; i++ )
    {

        // loop through all rows

        let row = fwd_mvs[i];
        var M_W = row.length/2;
        for ( let j = 0; j < row.length; j++ )
        {
            // loop through all macroblocks
            let mv = row[j];

            // THIS IS WHERE THE MAGIC HAPPENS
            //if(i>M_W){
				mv[0] = mv[0] + ((M_W - j) / 100)*zoom;
            	mv[1] = mv[1] + ((M_H - i) / 100)*zoom;
			//}
        }
    }
}
