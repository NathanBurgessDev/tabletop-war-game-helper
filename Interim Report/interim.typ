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

= Abstract 

= Introduction

- Gonna need to explain Kill Team in some way

== Motivation
Tabletop Wargaming is a popular hobby but, with a high barrier to entry, it remains niche and inaccessible to many. The rules to tabletop wargames can be complex and difficult to learn. This can be daunting for new players putting them off the hobby as well as causing arguments between seasoned players over different rules interpretations.

The most popular wargaming systems are produced by _Games Workshop_ @gw-size. One of their more popular systems, _Warhammer 40k_, has a core rulebook of 60 pages @40k-rules and the simplified version of another game system, _Kill Team_, is a rather dense three page spread @kt-lite-rules

Video games help on-board new players by having the rules of the game enforced by the game itself. This project aims to bring this experience to tabletop wargaming, specifically the _Kill Team Lite_ @kt-lite-rules  system. This is because the _Kill Team Lite_ rules are publically available from _Games Workshop's_ website and it is designed to be played on a smaller scale to other wargames, making it a good candidate for a proof of concept.

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

An RFID based approach is also used by _Steve Hinske_ and _Marc Langheinrich_ in their paper @rfid-based which places an antenna grid below the game board to detect RFID chips in pieces. This allowed them to find what chip is in range of what antenna, allowing them to find the general location of a game piece. This worked particularly well for larger models where you could put RFID chips far away from eachother on the model. Using the known positions of the chips and dimensions of the model combinded with which antenna said chips are in range of allows you to determine an accurate position of each model. They also go into alternate RFID approaches which I will discuss later when outlining my chosen methodology.

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

_STARS_ @STARS

_TARboard_

_UltraSound_

The systems previously mentioned use electronics embedded within the gameboard or within the game pieces to detect the position of minitures. As a result the average person would need specific hardware to use these systems.

== Project Description

This project aims to create a system that can track tabletop minitures, in a game of _Kill Team Gallowdark_, using only materials easily accessable to the average miniture wargamer. Then, utilise this system to implement a "helper" program for the game, providing a digital representation of the physical game state as well as rules enforcement.

As a result, the project can be broken down into two main goals.

#set enum(numbering: "1.a.")
+ Detection of the models and terrain to create a virtual representation of the game board.
    + The position of the miniture must be tracked accurately.
    + The system must be able to identify between different minitures.
    + The system must aim to be un-invasive to the minitures.
    + The system must be able to identify minitures regardless of what they look like.
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

One approach utilises increasing the range of an RFID reader to its maximum and then subsequently reducing the range repeatedly. Using the known ranges of the readers it would be possible to deduce which tags are within range of which reader - and subsequently deduce from which ranges it is detectable in the position of the RFID chip. This approach could in theory provide a reasonably accurate position of the RFID chip. However, this approach would take a longtime to update as each RFID reader would need to perform several read cycles. Combined with problems caused from interference between the chips / readers, the fact that being able to vary the signal strength of an RFID reader is not a common feature and the need for multiple RFID reachers, this approach does not meet the requirements for this project.

Another approach utilises measuring the signal strength recieved from an RFID chip and estimating the distance from the reader to the chip, known as received signal strength indication (RSSI) . This approach is much quicker than the previous method needing only a single read cycle to determine distance. Most modern day RFID readers can report RF phase upon tag reading. However, current RSSI methods have an error range of \~60cm caused by noise date, false positives / negatives and NLOS (non-line of sight) @RSSI.

Triliteration is a process in which multiple receivers use the time of arrival signal from a tag to detmine it's position. This suffers from similar problems to other RFID methods in that it produces an area in which the tag could exist within - as opposed to it's exact position. Combined with the need for 3 RFID receaders, this approach fails to be accessable to the target audience.

The approach previously mentioned in _Steve Hinske_ and _Marc Langheinrich_'s paper, which utilised an antenna grid below the gameboard, seemed promising. 

#figure(
    image("images/rfidCircle.png",width:60%),
    caption:([An example from _Steve Hinske_ and _Marc Langheinrich_'s paper @rfid-based describing their overlapping approach. The black square represents the RFID tag whilst the grey circles show the read area of each RFID reader. The intent is to use which readers are in range of the tag to determine an "area of uncertenty" of the tag's location.])
)

This approach worked rather well for _Steve Hinske_ and _Marc Langheinrich_ as they were attempting to do this for _Warhammer 40k_ a game played on a much larger space typically with larger models. As a result they were able to put RFID tags across larger models, such as vehicles, and utilise the known position of each tag relative to the model and the estimated position from the RFID readers to determine not only an accurate position but also orientation. Unfortunatly for this project the size of the minitures in _Kill Team_ would prohibit me to using one tag or two in very close proximity. 

A potentially valid method utilising RFID could be to use the approach outlined by _Zhongqin Wang, Ning Ye, Reza Malekian, Fu Xiao, and Ruchuan Wan_ in their paper @rfid-tracking using first-order taylor series approximation to achieve mm level accuracy called _TrackT_.

// Probably remove this - repetative
// There is a long list of methodologies that could be used to find and track minitures on a physical game board. However, finding an approach that can meet our aims of being able to both accurately track a minitures position and identify between them whilst also requiring the minimal amount of specialist hardware is a challenge.


=== IR

=== Touch Screen

The Last Gameboard

=== Computer Vision 

Surfacescapes 
Material Plane Module
TARboard
If the game breaks you can still play the physical game without the digital component.

=== Machine / Deep Learning

- YOLO?
- Lots of different ML approaches
- Size of dataset must be big
- Problems with identifying specific minitures
- Problematic when minitures will have similar paint schemes and poses - could be solved by looking at last known positions?
- Difficulty in keeping objects "unique"

Modern object tracking systems are often based on a machine learning or deep learning approach. In this case a classifier model would be used to identify each unqiue miniture on a team, and then subsequently locate it within the game board. The biggest drawback to this approach is the amount of training data needed for each class in a classifier. According to _Darknet's_ documentation (a framework for neural-networks such as YOLO) @yolo each class should have ~2000 training images.

Since each user will use their own minitures, posed and painted in their own way, they would have to create their own dataset for their minitures and train the model on them each time. As a user's minitures are likely to follow a similar paintscheme, ML classification could potentially struggle to indentify between minitures from top down and far away if not enough training data is supplied.

A solution to maintaining each minitures "unique identity" is to use the last known position combined with knowledge of what has moved in the game state. Though this process will be examined in more detail later.

Another issue with utilising ML is that it is computationally intensive. Whilst this 


=== ARKit

_Apple's_ ARKit supports the scanning and detection of 3D objects @ARKit by finding 3D spatial features on a target. Currently any phone running IOS 12 or above is capable of utilising the ARKit. In this system, you could scan in your models, then use the ARKit to detect them from above. This information could then be conveyed to the main system. This could also allow for the system to be expanded in the future to use a side on camera as opposed to just top down detection, allowing for verticality within other _Kill Team_ game systems. Combined with certain apple products having an inbuilt LIDAR sensor (such as the _iPhone 12+ Pro_ and _iPad Pro_ 2020 - 2022), which further enhances the ARKit's detection, this could be a viable approach.

#figure(
    image("images/LIDAR.png", width:80%),
    caption:([Registering an an object in ARKit @ARKit])
)

After some testing utilising an iPad Pro with a LIDAR scanner, some drawbacks were found with this approach. The object detection required you to be too close to the models detect them, and when being removed and re-added ARKit either took a long time to re-locate a model or failed to do so at all.

As a result I won't be using this approach for the project. Allthough, for future work, this could be an interesting option to explore allowing you to implement AR features such as highlighting models on your phone or tablet or displaying information above the model.

=== Ultrasound


= Methodology, Design and Implementation

// herefore, video analysis certainly is one of the most promising
// techniques for years to come. @rfid-based

== Design - Talk about Open CV, why the cameras are the way they are and why I chose to use python as well as the library for the digital part.

= Progress 

== Project Management 

== Contributions and Reflections 

#pagebreak()
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