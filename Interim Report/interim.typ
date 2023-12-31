#import "interimTemplate.typ": *

#set page(numbering: "1",number-align: center)
#show: diss-title.with(
    title: "Mixed Reality Tabletop War Game Assistant",
    author: "Nathan Burgess",
    ID: "20363169",
    email: "psynb7",
    programme: "BSc Computer Science",
    module: "COMP3003",
)

#pagebreak()
#outline(title: "Table of Contents")

// Number all headings
#set heading(numbering: "1.1.")

// Tweak space above and below headings
#show heading: set block(above: 2em, below: 1.3em)

// Justified paragraphs
#set par(justify: true)
#pagebreak()

= Introduction and Motivation

Tabletop Wargaming is a popular hobby but, with a high barrier to entry, it remains niche and inaccessible to many. The rules to tabletop wargames can be complex and difficult to learn. This can be daunting for new players putting them off the hobby as well as causing arguments between seasoned players over different rules interpretations.

The most popular wargaming systems are produced by _Games Workshop_ @gw-size. One of their more popular systems, _Warhammer 40k_, has a core rulebook of 60 pages @40k-rules and the simplified version of another game system, _Kill Team_, is a rather dense three page spread @kt-lite-rules

_Kill Team_ is a miniture wargame known as a "skirmish" game. This means the game is played on a smaller scale with only ~/20 minitures on the table at one time. The aim of the game is to compete over objectives on the board for points. Each player takes turns activating a miniture and performing actions with it. These actions can involing moving to another location, shooting at an enemy or capturing an objective. The game uses dice to determine the results of your models engaging in combat with eachother. 

#figure(
    image("images/gallowdark.jpg", width:80%),
    caption:([An example of the _Kill Team_ tabletop game using the _Gallowdark_ terrain])
)

Video games help on-board new players by having the rules of the game enforced by the game itself. This project aims to bring this experience to tabletop wargaming, specifically the _Kill Team Lite_ @kt-lite-rules  system using the _Gallowdark_ setting. This is because the _Kill Team Lite_ rules are publically available from _Games Workshop's_ website and it is designed to be played on a smaller scale to other wargames, making it a good candidate for a proof of concept. As well as this, the _Gallowdark_ @gallowdark setting streamlines the terrain used and removes verticality from the game, making implementation much simpler.

Developing a system that can accurately track the position of minitures and terrain in a _Kill Team_ board would allow for the creation of various tools to assist in the game. In this case a digital game helper would move the burden of rules enforcement and onto the system, allowing players to focus on the game itself or allow players to make more informed game decisions by being able to preview the options available to them. Model tracking could also be utilised to record a game and view a replay of it or be utilised for content creation to create accurate board representations to viewers with visual affects.

== Related Work

Previous attempts at created mixed reality tabletops fall into 2 categories. augmented / virtual reality or physical to digital. This will take a focus on a physical to digital approach as being able to use the minitures you built and painted yourself is an important part of the wargaming hobby.

Physical to digital systems use a physical game board and some detection system to find the pieces on the board. These can be further split into two categories, detection from above and detection from below.

=== Previous Mixed Reality Tabletops 

Some companies, such as _The Last Game Board_ @last-game-board and _Teburu_ @teburu, sell specialist game boards to provide a mixed reality experience. 

_The Last Game Board_ achieves this through utilising the touch screen to recognise specific shapes on the bottom of minitures to determine location and identity. _The Last Gameboard_ is 17"x17", as a result the number of game systems which are compatable is limited. However, you can connect multiple systems together. The drawback of this is the pricepoint for the system is rather high, with boards starting at \~\$350.
#figure(
image("images/theLastGameBoard.png", width:80%),
caption: [The Last Game Board touchscreen tabletop system @last-game-board])

_Teburu_ @teburu instead takes an RFID based approach, providing a base mat that allows you to connect squares containing RFID recievers and game pieces containing an RFID chip. _Teburu_ connects to a tablet device to provide the digital experience as well as to multiple devices for indvidual player information. _Teburu_ games allow for game pieces to either be in pre-determined positions or within a vague area i.e. within a room.

#figure(
image("images/teburu.jpg", width:80%),
caption:([The Teburu Game System @teburu-video showcasing _The Bad Karmas_ board game. The black board is the main game board. The squares above connect to the board below to transmit the RFID reader information back to the system for display.])
)

An RFID based approach is also used by _Steve Hinske_ and _Marc Langheinrich_ in their paper @rfid-based which places an antenna grid below the game board to detect RFID chips in pieces. This allowed them to find what chip is in range of what antenna, allowing them to find the general location of a game piece. This worked particularly well for larger models where you could put RFID chips far away from eachother on the model. Using the known positions of the chips and dimensions of the model combined with which antenna said chips are in range of allows you to determine an accurate position of each model. They also go into alternate RFID approaches which will be discussed later when outlining the chosen methodology.

//  INSERT IMAGE
#figure(
    grid(
    columns: 2,
    image("images/rfid-plane.png",width:80%),
    image("images/rfid-software.png",width:80%)),
    caption: "An example of Steve Hinske and Marc Langheinrich's approach depicting the antenna grid, RFID tags and physical model alongside the computer's prediction of the model's position"
    )
_Surfacescapes_ @surfacescapes is a system developed in 2009 by a group of masters students at Carnegie Mellon as a university project. _Surfacescapes_ uses a _Microsoft Surface Tabletop_ (the product line was rebranded to _PixelSense_ in 2011). This uses a rear projection display, and 5 near IR cameras behind the screen @pixelsense-specs. This allows the _PixelSense_ to idenify fingers, tags, and blobs touching the screen using the near IR image. _Surfacescapes_ utlises this tag sensing technology to track game pieces using identifyable tags on the bases of minitures.

#figure(
    image("images/surfacescapes.jpg",width:80%),
    caption:([An example of _surfacescapes_' in use on the _Microsoft Surface Tabletop_@surfacescapes-images. The position of the models have been tracked by the system and outlined with a green cricle.])
)

_Foundry Virtual Tabletop_ @foundry is an application used to create a fully digital _Dungeons and Dragons_ tabletops. These can either be used for remote play or in person play using a horizontal TV as a gameboard. _Foundry VTT_ allows for the creation of modules to add new functionality to your virtual tabletop. One such module is the _Material Plane_ @material-plane module which allows the tracking of physical minitures on a TV game board. This functions by placing each miniture on a base containing an IR LED with an IR sensor then placed above the board. This can be configured to either move the closest "virtual" model to where the IR LED is or (with some internal electronics in the bases) can be set up to flash the IR LED in a pattern to attatch different bases to specific models. An indicator LED is present to show when the IR LED is active.

#figure(
    image("images/foundry.jpg",width:60%),
    caption:([An example of  one of the _Material Plane_ bases. A miniture would be attatched to the top. @material-plane-github.])
)

// _STARS_ @STARS

// _TARboard_

// _UltraSound_

// Some of the systems previously mentioned use electronics embedded within the gameboard or within the game pieces to detect the position of minitures. As a result the average person would need specific hardware to use these systems.

== Project Description

This project aims to create a system that can track tabletop minitures, in a game of _Kill Team Gallowdark_, using only materials easily accessable to the average miniture wargamer. Then, utilise this system to implement a "helper" program for the game, providing a digital representation of the physical game state as well as rules enforcement.

As a result, the project can be broken down into two main goals.

#set enum(numbering: "1.a.")
+ Detection of the models and terrain to create a virtual representation of the game board.
    + The position of the miniture must be tracked accurately.
    + The system must be able to identify between different minitures.
    + The system must aim to be un-invasive to the minitures.
    + The system must be ambivalent to a model's shape and colour.
    + The system must be able to complete this task whilst being accessible to the average miniture wargamer.
+ Implementing the game logic in the virtual board to guide players through the game.
    + Allow users to select a model and a subsequent action (normal move, shoot, dash, capture objective).
    + Calculate the distance a model can move and display this on the virtual board.
    + Account for terrain that blocks movement.
    + Calculate the line of sight between the selected model and opposing models then display this on the virtual board.
    + Account for terrain that blocks line of sight.
    + Display information about the selected model's odds to hit a target.


= Methodology and Design

Finding a method to detect and find the positions of a minitures on a game board, while not obstructing the game, is a challenge. The majority of the work done so far has been in researching and designing different approaches to this problem. This section will outline the different approaches that have been considered.

== RFID

An RFID approach is the somewhat obvious solution. This would involve embedding RFID chips underneath the bases of the minitures. Then some method of reading these chips would then need to be embedded ether within or underneath the gameboard. There are a number of different approaches that could be taken to locating RFID chips which have been outlined by _Steve Hinske_ and _Marc Langheinrich_ @rfid-based in their work on a similar project.

RFID solutions would require either an antenna grid underneath the gameboard or multiple individual RFID readers. This would be a viable option as hiding an antenna grid below a board is a relatively simple and unobstructive task. The same goes for hiding RFID readers beneath a table.

The main drawback of RFID is that a reader (at its core) can only detect if a chip is in range or not (referred to as "absence and presence" results). Due to this, some extra methodology would need to be implemented to determine the position of a chip.

One approach utilises increasing the range of an RFID reader to its maximum and then subsequently reducing the range repeatedly. Using the known ranges of the readers it would be possible to deduce which tags are within range of which reader - and subsequently deduce from which ranges it is detectable in the position of the RFID chip. This approach could in theory provide a reasonably accurate position of the RFID chip. However, this approach would take a longtime to update as each RFID reader would need to perform several read cycles. Combined with problems caused from interference between the chips / readers, the fact that being able to vary the signal strength of an RFID reader is not a common feature and the need for multiple RFID readers, this approach does not meet the requirements for this project.

Another approach utilises measuring the signal strength recieved from an RFID chip and estimating the distance from the reader to the chip, known as received signal strength indication (RSSI) . This approach is much quicker than the previous method needing only a single read cycle to determine distance. Most modern day RFID readers can report RF phase upon tag reading. However, current RSSI methods have an error range of \~60cm caused by noise data, false positives / negatives and NLOS (non-line of sight) @RSSI. This won't work for this project given than the board size is 70 x 60 cm.

Triliteration is a process in which multiple receivers use the time of arrival signal from a tag to detmine it's position. This suffers from similar problems to other RFID methods in that it produces an area in which the tag could exist within - as opposed to it's exact position. Combined with the need for 3 RFID receaders, this approach fails to be accessable to the target audience.

The approach previously mentioned in _Steve Hinske_ and _Marc Langheinrich_'s paper, which utilised an antenna grid below the gameboard, seemed promising. 

#figure(
    image("images/rfidCircle.png",width:60%),
    caption:([An example from _Steve Hinske_ and _Marc Langheinrich_'s paper @rfid-based describing their overlapping approach. The black square represents the RFID tag whilst the grey circles show the read area of each RFID reader. The intent is to use which readers are in range of the tag to determine an "area of uncertainty" of the tag's location.])
)

This approach worked rather well for _Steve Hinske_ and _Marc Langheinrich_ as they were attempting to do this for _Warhammer 40k_ a game played on a much larger space typically with larger models. As a result they were able to put RFID tags across larger models, such as vehicles, and utilise the known position of each tag relative to the model and the estimated position from the RFID readers to determine not only an accurate position but also orientation. Unfortunatly for this project the size of the minitures in _Kill Team_ would prohibit me to using one tag or two in very close proximity. 

A potentially valid method utilising RFID could be to use the approach outlined by _Zhongqin Wang, Ning Ye, Reza Malekian, Fu Xiao, and Ruchuan Wan_ in their paper @rfid-tracking using first-order taylor series approximation to achieve mm level accuracy called _TrackT_. However, this approach is highly complex and can only track a small amount of tags at a time.

// READ THIS AND EXPLAIN

=== Machine / Deep Learning

// - YOLO?
// - Lots of different ML approaches
// - Size of dataset must be big
// - Problems with identifying specific minitures
// - Problematic when minitures will have similar paint schemes and poses - could be solved by looking at last known positions?
// - Difficulty in keeping objects "unique"

Modern object tracking systems are often based on a machine learning or deep learning approach. In this case a classifier model would be used to identify each unqiue miniture on a team, and then subsequently locate it within the game board. The biggest drawback to this approach is the amount of training data needed for each class in a classifier. According to _Darknet's_ documentation (a framework for neural-networks such as YOLO) @yolo each class should have ~2000 training images.

Since each user will use their own minitures, posed and painted in their own way, they would have to create their own dataset for their minitures and train the model on them each time. As a user's minitures are likely to follow a similar paintscheme, ML classification could potentially struggle to indentify between minitures from top down and far away if not enough training data is supplied.


=== ARKit

_Apple's_ ARKit supports the scanning and detection of 3D objects @ARKit by finding 3D spatial features on a target. Currently any phone running IOS 12 or above is capable of utilising the ARKit. In this system, you could scan in your models, then use the ARKit to detect them from above. This information could then be conveyed to the main system. This could also allow for the system to be expanded in the future to use a side on camera as opposed to just top down detection, allowing for verticality within other _Kill Team_ game systems. Combined with certain Apple products having an inbuilt LIDAR sensor (such as the _iPhone 12+ Pro_ and _iPad Pro_ 2020 - 2022), which further enhances the ARKit's detection, this could be a viable approach.

#figure(
    image("images/LIDAR.png", width:80%),
    caption:([Registering an an object in ARKit @ARKit])
)

After some testing utilising an iPad Pro with a LIDAR scanner, some drawbacks were found with this approach. The object detection required you to be too close to the models detect them, and when being removed and re-added ARKit either took a long time to re-locate a model or failed to do so at all.

As a result I won't be using this approach for the project. Allthough, for future work, this could be an interesting option to explore allowing you to implement AR features such as highlighting models on your phone or tablet or displaying information above the model.

=== Computer Vision without neural networks

After considering all the options above, the best method found was using computer vision techniques.

One technique is blob detection. A blob is defined as a group of bright or dark pixels contrasting against a background. In this case the minitures would be the blobs.

Utilising blob analysis would allow locating general position of minitures (as they would very clearly stick out from the background) but getting their exact center may then prove difficult (which would be needed for calculating movement and line of sight). Combined with the addition of terrain adding clutter to the image and the minitures potentially being any colour, this approach could prove difficult to implement in the given timeframe.

The computer vision method explored the most was utilising coloured tags to identify minitures.

The use of coloured tags would also mean there would be access to specific measurements allowing for an accurate location to be discerned. However, some external modifciation to the the gameboard or minitures would need to be made. The challenge here is finding a way to do this without obstructing the flow of the game or the models themselves.

= Methodology, Design and Implementation

// herefore, video analysis certainly is one of the most promising
// techniques for years to come. @rfid-based

== Design - Talk about Open CV, why the cameras are the way they are and why I chose to use python as well as the library for the digital part.

The general design of the system would placewebcam or camera above the gameboard. Minitures would have easily recognisable tags attatched to allow for easy identification via computer vision.

The tag would need to be unobstructive to the game (big enough to be seen by the camera but small enough as to not get in the way of the game whilst also not looking too "out of place"). This ruled out sticking QR codes ontop of minitures, or attatching them to wires above the minitures. This meant a unique design was needed.

Before we start trying to find tags we should first perform some viewpoint / perspective correction. Our end goal is to get a birds eye view of the gameboard, however a camera placed above the board will produce a slightly distorted view of the gameboard. This process would involve finding some set reference points on the board, in this case the corners, and using these to perform a perspective transform creating a top down view of the image. This means that when the tags are located we can provide their location directly to the gameboard display.

The detection problem can be split into two components: locating and identifying the miniture. Tackling the location problem first seemed like the most sensible approach to begin with before moving onto identification.

In the end it was chosen to 3D print a small rim that could fit around the base of a miniture. This rim would be a high contrasting colour to the background and miniture. The benefits of 3D printing the rim is that the colours and dimensions are customizable to the user. Miniture wargamers paint their models in a variety of different ways, so having a rim they can decide the colour of themselves keeps the system accessable to the target audience and open to many different miniture sizes and colours. 

#figure(
    image("images/circleYellow.jpg",width:50%,),
    caption: ([An example of the basic contrasting rim design.])
)

Some important observations here are that models may poke over the edge of the rim and models will block the rim due to parallax, so a rim detection system will need to find a full circle from only a partial amount of visable rim. When terrain is introduced this will cause further issues The proposed fixes for this will be discussed later.

The next step was to find a way to detect the rim. The best solution found for this was _openCV_ @openCV. An alternative image processing suit would have been to utilise _MATLAB_, but _openCV_ can be used directly within _Python_. As a result, the final system could be written entirely within _Python_ signficantly streamlining the development process without needing to connect MatLab with an external program for the game board logic / display. 

This led to the development of a processing method which will locate the center point of circles of a specific colour in a provided image. 

The image processing steps taken:

// REMEMBER TO QUOTE THIS: https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html

+ Sort the image to only contain the colour of the rim (in this case yellow).
+ Greyscale the image.
+ Apply a blur to the image (this helps to remove noise from the image).
+ Apply hough circle detection @hough-circles on the processed image.
+ Draw the detected circles onto the original image.

It is important to note that hough circle detection can easily mistake two close but separate circles as one circle. As a result of this, the hough circle detection function in _openCV_ has several arguments that will need to be tweaked as the system is developed.

Through some testing we were able to locate singular circles even with the presence of terrain pieces blocking parts of the rim. 

#figure(
    image("images/detection.png",width:80%),
    caption: ([Circle detection on a gameboard with example terrain.])
)

Parallax is a problem that still needs to be addressed. Through testing it was found that using a standard gameboard size, the parallax was too great to expect to locate a rim. As a result, we have settled on using a two camera solution. This solves the parallax problem by having each camera watch a different half of the gameboard.

However, one problem with this approach is that calibration will be needed to ensure that the overlap between the cameras does not cause issues. This could be achieved by either calibrating the cameras to the game board, as it will be of a known size, by placing tags on each corner of the board. Alternatively the middle of the board could be marked with a piece of tape, or tags on the edges. This should then allow for the two images to be stitched together accuratly.

Due to the nature of this project being aimed at following the _Kill Team Gallowdark_ ruleset, the terrain pieces used are placed along a grid. This prevents a situation where a terrain piece is very close to the edge of a board with a miniture placed behind resulting in the miniture being blocked from view. 

// PROVIDE SOME IMAGE TO DESCRIBE THIS. CITE OPEN CV AND MATLAB

// MinDist - min distanceb etween the centers of two circles, 
// param1 - sensitivity of the canny edge detection - 
// param2 - how close to a full circle is needed for it to be detected - number of edge points needed to declare a circle.
// minRadius + maxRadius - pretty self explanitory - closer or further to camera

// - One potential tracking approach is explored by this video: 
// https://www.youtube.com/watch?v=RaCwLrKuS1w
// - Looks at a circle in the newest frame that is closest in position and size to the tracked circle in the last frame.
// - We can exploit the fact that _Kill Team_ is turn based such that only one model can move at a time. Due to this we can compare the differences between the previous image of the game state and the current game state to indentify which model has been moved.
// - This can assist in making up for shortcomings in the identifcation methods.

Once we have located a model we need to identify it. In our implementation of _Kill Team_ we will assume that each player will have up to 14 models on their team (known as "operatives"). As a result we will need to create an encoding capable of representing at least 28 different options.

Another rim will be placed around the bright contrast rim from before. This rim will be split into 6 sections. The first section will indicate the starting of the encoding and will use a unique colour. The other 5 sections will use 2 different colours to represent 1 or 0. Once a rim has been located, the system will then determine the orientation of the encoding circle. As the size is known, we can then rotate around the image of the encoding circle reading each section to eventualy get a binary number. Each binary number will then represent a unique model on the board.

#figure(
    image("images/circle.png",width:60%),
    caption: ([An example of what the encoding circle could look like. The red section indicates the start of the encoding. The system would be able to determine which direction to read in based on the start encoding section being in the bottom or top half of the image.])
)

Another encoding method that was considered was to use one rim for both detection and identification. By using one rim of known colours, the image could be split into 3 images each containing only the colour of each segment. Each image would then be converted to black and white and recombined to create a singular image with the segments connected to create a full circle. After circle detection has been performed the system could then do the normal encoding reading. This approach would allow the rims of the minitures to be significantly smaller and only require three contrasting colours.

One problem faced by this approach is that vision of the entire circle is needed to read the encoding, as a result if it is partially obscured then the system will be unable to identify the model.

This could be counteracted by splitting the encoding into quarters around the rim, so that as long as 1/4 of the encoding is visable, the system can correctly identify it. We can also exploit _Kill Team_ being a turn based game and simply compare the current game state with the previous game state to identify which pieces have been moved. A combination of active tracking and being able to determine which piece has moved, should allow for a robust system.

Terrain detection will be performed using two possible solutions, the user can either select pre-determined terrain set ups or the system can detect the terrain pieces.

The current approach for terrain detection is to use QR codes on the top of each terrain piece. In _Gallowdark_ the size and shape of each terrain "module" is already known. As a result, the QR code can be used to determine the type of terrain and orientation. Then, since the terrain type has been established we already know the size and shape. So we can then fill it in on the virtual board.

Once the system has correctly identified and located each model and the terrain, a digital representation of the gameboard can be created.

#figure(
    image("images/board-suggestion.png"),
    caption: ([A proposed GUI for the game helper.])
) <GUI>

In @GUI the red semi-circle represents the valid area of movement for a selected operative. This can be calculated by splitting the game board into a very small grid, we can then apply a pathfinding algorithm (Dijkstra's, A\* etc) to the grid from the operatives starting point. We can then calculate all grid positions reachable by using a movement value less than or equal to the current operatives available movement characteristic.

Red circles around opposing opperatives show they are in line of sight. This would be calculated using simple ray casting. A white and red circle indicates a selected opposing opperative. This is to calculate the statistics on the right hand side of the screen to be specific to the opposin opperative.

The information for the selected operative is displayed below the gameboard. A user can select the action they have performed / want to perform on the right hand side.

The GUI will be built in _PyQt_ @pyqt which is a python wrapper for the _Qt_ framework. One potential strech goal is for the GUI and the detection system to be seperate entities. For example, the detection system should be able to detect and track pieces without input needed from the virtual gameboard i.e. which model is selected. This would allow for other detection systems to be swapped out in the future or for other applications to be developed using the detection system.

= Progress 

== Project Management

As per the inital Project Proposal the original goal for the first semester was to have ring detection and terrain detection completed. Currently, simple ring detection has been completed. This still needs to be expanded to include identification, though work has begun on this. Terrain detection has been moved backwards to allow for more time to make a good detection system for the minitures.

Choosing to tackle the ring detection first was a good choice. This allowed for me to encounter larger issues and provide solutions to them whilst still in the research stages on the project. This has allowed for me to develop my computer vision skills and take approaches I would not have otherwise considered. For example, using a singular rim of multiple colours and combining the images to create a full circle for identificaton.

Supervisor meetings were held every week to check for blockers or advice on reports. Uniquely, our supervisor meetings were conducted as a group with the other two dissertation students my supervisor had. As all three of us were working on tabletop game based projects we were all knowledgable in the area. This meant we could provide feedback or ideas for eachothers projects from a student perspective.

I found the GANNT chart to be unhelpful in managing the project. GANNT charts work well in well structured work environments.However, due to the nature of this semester having a large amount of other courseworks and commitments that needed to be balanced. An agile approach was much more effective, doing work when time was available. The nature of development work being much more effective when done in long, uninterupted sessions meant that, with this semesters courseworks and lectures being very demanding at 70 credits, being able to find long swathes of uninterupted time was very difficult between lectures, courseworks, tutorials etc. As a result, development was done in smaller, more frequent chunks which were not as effective as longer, less frequent chunks. I expect this to change next semester when the workload decreases down to 50 credits.

A much prefered method, that I will likely go ahead with, is Kanban. I personally found most use from the GANNT chart in that the project is naturally broken up into sub tasks. This type of subtasking when combined with a less structured agile approach is something that Kanban works really well at and have found effective in the past in GRP.

In the interests of being able to show current progress in comparison to previous I have included an updated GANNT chart (@firstGANNT) along the preivous one (@secondGANNT).

Looking at the time remaining I will focus on getting the main parts of the system functional. These are: model detection and tracking, terrain detection, virtual game board representation, movement preview and line of sight preview. If there is time available then I will aim to also implement the flow of the game (breaking it down into each phase, providing guidence of what to do in each phase, statistics etc). The most technically interesting part of this is the virtual game board and tracking technology. So placing a focus on having them work fluidly is more important to the dissertation.




#import "@preview/timeliney:0.0.1"

#page(flipped: true)[
#figure(
timeliney.timeline(
  show-grid: true,
  {
    import timeliney: *
      
    headerline(group(([*January*], 4)),group(([*February*], 4)),group(([*March*], 4)),group(([*April*], 4)),group(([*May*],3)))
    headerline(
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(3).map(n => strong(str(n + 1)))),
    )
  
    taskgroup(title: [*Other Commitments*], {
      task("MDP Coursework",(0,3.5), style: (stroke: 2pt + gray))
      task("HAI Coursework", (0, 1), style: (stroke: 2pt + gray))
      task("Ethics Essay",(0,3.5),style: (stroke: 2pt+gray))
      task("SEM Coursework", (6,12), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Initial Write-up*], {
      task("Interim Report", (0, 0.25), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Computer Vision*], {
      task("Multi Ring Tracking",(4,5),style: (stroke: 2pt + gray))
      task("Ring Identification", (5,7), style: (stroke: 2pt + gray))
      task("Terrain Detection", (7, 8), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Game Logic*], {
      task("Game Board Framework",(8,10), style: (stroke: 2pt + gray))
      task("Movement",(10,11), style: (stroke: 2pt + gray))
      task("Line of Sight",(11,12), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Final Write-up*], {
      task("Dissertation", (12, 14), style: (stroke: 2pt + gray))
      task("Presentation Prep", (14, 18.5), style: (stroke: 2pt + gray))
    })

    milestone(
      at: 0.25,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Interim Report Submission*\
        Jan 2023
      ])
    )

    milestone(
      at: 14,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Dissertation Submission*\
        Apr 2024
      ])
    )

    milestone(
      at: 18.5,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Project Presentation*\
        May 2024
      ])
    )
  }
),
caption: ([The Updated GANNT chart])
) <firstGANNT>
]


#page(flipped: true)[
#figure(
  timeliney.timeline(
  show-grid: true,
  {
    import timeliney: *
      
    headerline(group(([*October*], 4)), group(([*November*], 4)),group(([*December*], 4)),group(([*January*], 4)),group(([*February*], 4)),group(([*March*], 4)),group(([*April*], 4)),group(([*May*],3)))
    headerline(
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(4).map(n => strong(str(n + 1)))),
      group(..range(3).map(n => strong(str(n + 1)))),
    )
  
    taskgroup(title: [*Other Commitments*], {
      task("MDP Coursework", (4, 7),(7.2,13.75), style: (stroke: 2pt + gray))
      task("HAI Coursework", (2, 10), style: (stroke: 2pt + gray))
      task("Ethics Essay",(1,4),(6,9),(10.5,13.75),style: (stroke: 2pt+gray))
      task("SEM Coursework", (18, 24), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Initial Write-up*], {
      task("Project Proposal", (2,4), style: (stroke: 2pt + gray))
      task("Ethics Checklist", (4, 5), style: (stroke: 2pt + gray))
      task("Interim Report", (7.5, 9.5), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Computer Vision*], {
      task("Ring Detection", (3, 6), style: (stroke: 2pt + gray))
      task("Terrain Detection", (6, 8), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Game Logic*], {
      task("Game Board Framework",(13.75,16), style: (stroke: 2pt + gray))
      task("Movement",(16,18), style: (stroke: 2pt + gray))
      task("Line of Sight",(18,19), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Final Write-up*], {
      task("Dissertation", (22, 26), style: (stroke: 2pt + gray))
      task("Presentation Prep", (26, 30), style: (stroke: 2pt + gray))
    })

    milestone(
      at: 10,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Interim Report Submission*\
        Dec 2023
      ])
    )

    milestone(
      at: 26,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Dissertation Submission*\
        Apr 2024
      ])
    )

    milestone(
      at: 30.5,
      style: (stroke: (dash: "dashed")),
      align(center, [
        *Project Presentation*\
        May 2024
      ])
    )
  }
),
  caption: ([The original GANNT chart])
)<secondGANNT>
] 

== Contributions and Reflections 

Something I underestimated was the amount of time needed to research and determine which method should be used for model detection. A large amount of time was spent determining the viabiity of different approaches that may make the system more robust and easier to produce. As a result of this, development started later and took longer than was expected.

The biggest impact on this project was needing to get an extension on other coursework deadlines. This extension had a knock on effect of other courseworks which took priority over this project. The timings alloted in the GANNT chart did not take into account extensions being needed.

However, I am happy with the progress made so far. Having completed the methodology to find the circular tags even when partically obstructed is very promising to the viability of the chosen approach. As a result, I believe that a solid strategy has been chosen for model detection and identification and the work done so far has successfully laid a good foundation for the project.

=== LSEPI

The main LSEPI issue you could see here is copywright issues as _Kill Team_ is a copywrighted entity owned by _Games Workshop_. The way this project will handle this is by having the system implement the _Kill Team Lite_ ruleset previously mentioned. This is publically available published by _Games Workshop_. One issue is that different "_Kill Teams_" (groups of operatives) will have  different and unique rules as well as their own statistics pages. These are copywrighted and won't be able to be directly implemented. As a result of this, this project will implement basic operatives with fake statistic pages based off of the publically published _Kill Team_ information. If this proves to be problematic then the game rules will be based off a very similar system _Firefight_ @one-page. This is published by _One Page Rules_, who produce free to use, public miniature wargame systems.


= Bibliography

#bibliography(title: none, style: "ieee", "interim.yml")


// @article{article,
// author = {Lee, W. and Woo, Woontack and Lee, Jongweon},
// year = {2005},
// month = {01},
// pages = {0-4},
// title = {TARBoard: Tangible Augmented Reality System for Table-top Game Environment},
// volume = {5},
// journal = {Personal Computing}
// }


