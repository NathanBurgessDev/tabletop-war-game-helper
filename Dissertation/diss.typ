#import "interimTemplate.typ": *

#set page(numbering: "1",number-align: center)
#show: diss-title.with(
    title: "Mixed Reality Tabletop War Game Assistant",
    author: "Nathan Burgess",
    ID: "20363169",
    email: "psynb7",
    programme: "BSc Hons Computer Science",
    module: "COMP3003",
)

#let todo(body) = [
  #let rblock = block.with(stroke: red, radius: 0.5em, fill: red.lighten(80%))
  #let top-left = place.with(top + left, dx: 1em, dy: -0.35em)
  #block(inset: (top: 0.35em), {
    rblock(width: 100%, inset: 1em, body)
    top-left(rblock(fill: white, outset: 0.25em, text(fill: red)[*TODO*]))
  })
  <todo>
]

#let outline-todos(title: [TODOS]) = {
  heading(numbering: none, outlined: false, title)
  locate(loc => {
    let queried-todos = query(<todo>, loc)
    let headings = ()
    let last-heading
    for todo in queried-todos {
      let new-last-heading = query(selector(heading).before(todo.location()), loc).last()
      if last-heading != new-last-heading {
        headings.push((heading: new-last-heading, todos: (todo,)))
         last-heading = new-last-heading
      } else {
        headings.last().todos.push(todo)
      }
    }

    for head in headings {
      link(head.heading.location())[
        #numbering(head.heading.numbering, ..counter(heading).at(head.heading.location()))
        #head.heading.body
      ]
      [ ]
      box(width: 1fr, repeat[.])
      [ ]
      [#head.heading.location().page()]

      linebreak()
      pad(left: 1em, head.todos.map((todo) => {
        list.item(link(todo.location(), todo.body.children.at(0).body))
      }).join())
    }
  })
}

#pagebreak()
#outline(title: "Table of Contents",depth: 3, indent: auto)

// Number all headings
#set heading(numbering: "1.1.")

// Tweak space above and below headings
#show heading: set block(above: 2em, below: 1.3em)

// Justified paragraphs
#set par(justify: true)
#pagebreak()

#import "@preview/wordometer:0.1.1": word-count, total-words
#show: word-count

In this document, there are #total-words words all up.

= Abstract 

= Introduction and Motivation

Tabletop war-gaming is a popular hobby that is quickly gaining popularity, however, with a high barrier to entry, it remains niche and inaccessible to many. The rules to tabletop war-games can be complex and difficult to learn. This can be daunting for new players, putting them off the hobby as well as causing disagreement between seasoned players over rules interpretations.

Some of the most popular war-gaming systems are produced by _Games Workshop_ @gw-size. One of their more popular systems, _Warhammer 40k_, has a core rule-book of 60 pages @40k-rules and the simplified version of another game system, _Kill Team_, is a rather dense three page spread @kt-lite-rules. This complexity can be off putting to new players. Many tabletop / boardgames suffer from a players first few games taking significantly longer than is advertised due to needing to constantly check the rules.

As well as this, new players are likely to take longer to make decisions as they are not familiar with the game's mechanics of what constitutes a "good" move (sometimes referred to as "analysis paralysis"). This can be exacerbated by the game's reliance on dice rolls to determine the outcome of actions. Meaning that seemingly "optimal" moves do not always result in favourable outcomes, causing an extended learning period for an already complex game.

_Kill Team_ is a miniature war-game known as a "skirmish" game. This means the game is played on a smaller scale with only \~20 miniatures on the table at one time. The aim of the game is to compete over objectives on the board for points. Each player takes turns activating a miniature and performing actions with it. These a selection of actions are: moving to another location, shooting at an enemy, melee combat and capturing an objective. The game uses dice to determine the results of your models engaging in combat with each other with the required rolls being determined by the statistics of each "operative" (a miniature) involved and the terrain.

#figure(
    image("images/gallowdark.jpg", width:80%),
    caption:([An example of the _Kill Team_ tabletop game using the _Gallowdark_ terrain. The terrain we will focus on here are the flat walls and pillars. @gallowdark-image])
) <gallowdark-terrain>

Video games help on-board new players by having the rules enforced by the game itself. This project aims to bring a similar methodology to tabletop war-gaming, specifically the _Kill Team Lite_ @kt-lite-rules  system using the _Gallowdark_ setting. The _Kill Team Lite_ rules are publicly available from _Games Workshop's_ website and is designed to be played on a smaller scale to other war games, making it a good candidate for a proof of concept. As well as this, the _Gallowdark_ @gallowdark setting streamlines the terrain used and removes verticality from the game, making implementation much simpler.

Developing a system that can digitally represent a physical _Kill Team_ board would allow for the creation of tools to assist players. For example, a digital game helper would remove the burden of rules enforcement from the players and onto the system, allowing players to focus on the game itself or allow players to make more informed game decisions by being able to preview the options available to them. This could also be utilised to record a game and view a replay or be used for content creation to make accurate board representations to viewers with digital effects.

== Project Intention and Background

This project will focus on the development of a system that can track the position of miniature models and terrain pieces on a _Kill Team_ board which can subsequently be displayed digitally. From here, we aim to implement proof of concept visualisation of a few select game rules on the digital board to demonstrate that the tracking system provides the necessary information to process said rules.

To determine the specific goals for this project, it is important to provide some more context on the gameplay and community surrounding _Kill Team_. As this is a very complex game, we will be omitting a large percentage of the rules, focusing on the topics that will have an impact on the overall design or provide unique challenges.

=== Gameboard Components

Before looking at the game rules, we will first break down the physical components of the gameboard to determine what needs to be tracked and problems that may arrise from this.

A game of _Kill Team_ is comprised of two players, each with a group of "operatives" (miniatures) referred to as a "Kill Team". Each Kill Team has it's own unique rules, with each operative having it's own set of unique statistics and special abilities.  A miniature is comprised of a circular base with a model placed on top. The diameter of the base is either 25mm, 28.5mm, 32mm, 40mm or occasionally 50mm.

#figure(
  image("images/kasrkinExample.jpg", width:50%),
  caption:[An example of a _Kasrkin_ _Kill Team_ operative on a 28.5mm base @kasrkin-image. The height of the operative is \~35mm excluding the base. This project will focus on getting the system functional with the _Kasrkin_ models on 28.5mm bases.]
) <Kasrkin-Example-Figure>

It is worth noting that is is common for models to extend past the edge of their base as seen in @Kasrkin-Example-Figure. Whilst the example above is somewhat minor in its overlap, different models can be more extreme in their extension. As a result of this the system will need to be able to locate and identify an operative from only a partial view of the base, or its surroundings, from a bird's eye view. The detection system will either need to be above the board if using visual detection methods or below the board if using, for example, an RFID method. This is due to the terrain potentialy surrounding an operative, so having a camera on each side of the board will not guarantee it is visible.

The game is played on a 30" by 22" board, referred to as a "Killzone". The _Gallowdark_ ruleset instead uses a 27" by 24" board with the specialised terrain shown in @gallowdark-terrain. As stated previously, the terrain we are focusing on here are the thin walls with pillars connecting them. The terrain is all at the same height, but the operatives are shorter than the terrain. As a result, the system will need to find a solution to detect operatives behind terrain. From a birds eye view, the terrain will block part of the operative due to parallax. For this project, we will focus on using a half sized board to simplify this problem.

#figure(
  image("images/parallaxDiagram.svg", width:40%),
  caption:[An example of the problem introduced by parallax. The camera is placed above the board offset from the operative. The operative is partially obstructed by terrain. The green triangle represents the parts visible to the camera. The red lines demonstrate the areas blocked by the terrain.]
)

The further away the camera is from the operative on the x axis, the more the terrain will block the operative. However, as the camera travels away on the y axis, the terrain will block less of the operative. For a camera implementation this would also mean we lose quality in the image. As a result, a camera based system would need to find an ideal distance from the board which provides enough quality in the image, whilst also being able to see enough of an operative if it is obscured by terrain.

#todo("Put an IRL image in here to demostrate")
#pagebreak()
=== Gameplay

The gameplay of Kill Team focuses around a turn based system with a full game consisting of 4 rounds - called "turning points". Each player takes turns "activating" a single operative and performing actions with it. The number of actions available to an operative is defined by it's statistics #footnote("There are a lot of exceptions to this with abilities being able to modify the stats of themselves or other operatives, but for the sake of simplicity we are going to ignore this and assume stats are set."). Once an operative has performed it's maximum number of actions, play is handed to the other player. That same operative may not be "activated" until every other operative, still in play, on their team has been activated. Once every operative on both teams has been activated the next turning point begins resetting the activation of each operative still in play. Once all 4 turning points have been completed the game ends and a winner is decided.

This project is focussed on creating a digital representation of the board, and then implementing a few select rules from the game to demonstrate the system's capabilities. The rules for "movement" and "shooting" present themselves as good candidates for this due to both their complexity and frequency within the game.

Please note that the explanations for these rules are abstracted from the _Kill Team Lite_ rules published publicly by Games Workshop @kt-lite-rules.

==== Movement

There are two types of movement available: "normal move" and "dash". A normal move allows an operative to move a set distance as defined in it's statistics (typically this is 6"). A dash allows an operative to only move 3". Movement has several restrictions attatched.

#set enum(numbering: "1.a.")
+ Movement must not exceed the operative's movement characteristic.
+ Movement must be made in straight line increments. This means no curves but diagonals are fine.
  + Increments can be less than 1" but are still treated as 1" for the purpose of total movement.
+ An operative cannot move through terrain unless it is a "small obstacle" (such as a barricade) #footnote("We will not be encountering small obstacles in this implementation.")
+ An operative may not move over the edge of the board or through any part of another operative's base.
+ An operative CAN perform a normal move and dash in the same turn.
+ An operative CAN perform a normal move OR dash and then perform a "shoot" action.

This is quite a complex set of rules to enforce, making movement a good candidate for the system to assist with.

#todo("Maybe add some images to demonstrate")
==== Shooting and Line of Sight

Operatives can be set to two states: "concealed" or "engaged". These states are used to determine whether an operative is a valid target or whether it is able to make offensive actions, such as shooting. An operatives state is denoted by a small triangle of orange card pointing to the model. The system will need a way to track the state of an operative, whether this be through detecting the orange markers or manually updating the state.

Anecdotally, the _Kill Team_ line of sight rules tend to be the most complex part of the game and are constructed in such a way that experienced players can abuse them to gain an advantage such as one way shooting#footnote("This is a technique used to allow an attacker to be able to select a valid target but the defender is unable to fire back.").

#figure(
  image("images/orders.jpg",width:40%),
  caption: [An example of the markers used to denote the state of an operative @order-image. Once an operative has been activated the marker is flipped.]
)

There are a set of requirements that must be met to determine whether a target is able to targeted by a shooting attack.
We will use *attacker* to refer to the operative making the attack and *defender* to refer to the intended target.

For a defender in the engaged state:

+ The defender must be *visible*.
+ The defender must be not *obscured*.

For a defender in the concealed state:

+ The defender must be *visible*.
+ The defender must be not *obscured*.
+ The defender must be not *in cover*.

_Kill Team_ defines *visible*, *obscured* and *in cover* very strictly. This is done using *cover / visibility lines* which are straight lines 1mm wide drawn from one point on an operative to another operative.

===== Visible

*Visible* is used to simulate whether a defender can be physically seen by an attacker

For a defender to be (visible) the following must be true:

+ A visibility line can be drawn from the head of the attacker to any part of the defenders *model*, not including the base.

===== Obscured

*Obscured* is used to simulate whether a defender is blocked by large terrain, such as a wall, while also containing edge cases for operatives peeking round said terrain or attempting to use it directly as cover.

When drawing cover lines the attacker picks one point on their base and draws two cover lines from that point to every point on the defenders base, to create a cone. In practice this means drawing two cover lines to the extremes of the defenders base.

#todo("Going to need to put some examples in - maybe use the pre-existing ones? not sure if this is ok to use: https://www.reddit.com/r/killteam/comments/vukgpz/basic_line_of_sight_rule_slate_i_made_for_our/#lightbox")

For a defender to be *obscured* the following must be true:

+ The defender is >2" from a point where a cover line crosses a terrain feature which is considered obscuring#footnote("For our use case the terrain walls in Gallowdark are all considered obscuring terrain.").
  + If the attacker is \<1" from a point in which a cover line crosses a terrain feature, then that part of the feature is not obscuring.

===== In Cover

*In cover* simulates whether an operative is attempting to intentionally take cover behind piece of terrain. A concealed operative is hiding behind the terrain whereas an engaged operative is poking around / over it.

For a defender to be *in cover* the following must be true:

+ The defender is >2" from the attacker
+ The defender is \<1" from a point where a cover line crosses a terrain feature.

There are a few key takeaways from these rules.

+ It is important to know the positions of operatives and terrain.
+ The system will need to be able to know the size of an operative's base.
+ Rotation of operatives is not needed to be tracked (except for visiblity when determining *visible*).
+ Operatives need to be marked as concealed or engaged.
+ Accuracy is important to the system. Visiblity / cover lines being 1mm wide and distances measured in inches will require accurate measurements.
+ The system will need to asbtract the above rules whilst also being able to display the reasoning behind the application. For example, if a defender is obscured the system should show what is obscuring and from what point was the firing cone drawn.

=== Community

Tabletop wargames require you to build and paint your own minitatures, because of this the target audience tends to be more of the creative type. Using this information we can allow some liberty in what they might need to do to utilise this system. For example, creating homemade tags is something that creatives might be more inclined to do as opposed to something more technical using RFID or infrared sensors. The whole system should be designed to be as accessible as possible to the target audience, requiring little to no specialised equipment.

The minitatures are also not defined in their appearance. They can be painted in any scheme, be customised to have completely different looks or use entirely different models than what is intended#footnote("Known as proxying."). This means the tracking system needs to be ambivolent of what the model looks like, both in colour and silhouette.

Since miniatures are highly customisable players tend to be very attatched to them. So one important requirement is to not be invasive to the miniature. This rules out requiring a certain paintjob, placing stickers on heads or putting QR codes above operatives. The system should aim to obscure models as little as possible and cause no damage.

#pagebreak()
= Related Work

== Previous Mixed Reality Tabletop Systems

Some companies, such as _The Last Game Board_ @last-game-board and _Teburu_ @teburu, sell specialist game boards to provide a mixed reality experience. 

_The Last Game Board_ achieves this through utilizing the touch screen to recognise specific shapes on the bottom of miniatures to determine location and identity. _The Last Gameboard_ is 17" x 17", as a result the number of game systems which are compatible is limited. However, you can connect multiple systems together. The drawback of this is the price point for the system is rather high, with boards starting at \~\$350. It is also worth noting that this system has not recieved great reviews, with alpha users reporting: long load times, low FPS, graphical and sound glitches, lack of updates and even screens refusing to display half the screen for certain applications.
#figure(
image("images/theLastGameBoard.png", width:70%),
caption: [The Last Game Board touchscreen tabletop system @last-game-board])

_Teburu_ @teburu instead takes an RFID based approach, providing a base mat that allows you to connect squares containing RFID receivers and game pieces containing an RFID chip. _Teburu_ connects to a tablet device to provide the digital experience as well as to multiple devices for individual player information. _Teburu_ games allow for game pieces to either be in predetermined positions or within a vague area i.e. within a room.

#figure(
image("images/teburu.jpg", width:80%),
caption:([The Teburu Game System @teburu-video showcasing _The Bad Karmas_ board game. The black board is the main game board. The squares above connect to the board below to transmit the RFID reader information back to the system for display.])
)

An RFID based approach is also used by Steve Hinske and Marc Langheinrich in their paper @rfid-based which places an antenna grid below the game board to detect RFID chips within models. This allowed them to find what chip is in range of what antenna, allowing them to find the general location of a game piece. This worked particularly well for larger models where you could put RFID chips far away from each-other on the model. Using the known positions of the chips and dimensions of the model combined with which antenna said chips are in range of allows you to determine an accurate position of each model. They also go into alternate RFID approaches which will be discussed later when outlining the chosen methodology.

//  INSERT IMAGE
#figure(
    grid(
    columns: 2,
    image("images/rfid-plane.png",width:80%),
    image("images/rfid-software.png",width:80%)),
    caption: "An example of Steve Hinske and Marc Langheinrich's approach depicting the antenna grid, RFID tags and physical model alongside the computer's prediction of the model's position"
    )
_Surfacescapes_ @surfacescapes is a system developed in 2009 by a group of masters students at Carnegie Mellon as a university project. _Surfacescapes_ uses a _Microsoft Surface Tabletop_ (the product line was rebranded to _PixelSense_ in 2011). This uses a rear projection display, and 5 near IR cameras behind the screen @pixelsense-specs. This allows the _PixelSense_ to identify fingers, tags, and blobs touching the screen using the near IR image. _Surfacescapes_ utilises this tag sensing technology to track game pieces using identifiable tags on the bases of miniatures.

#figure(
    image("images/surfacescapes.jpg",width:80%),
    caption:([An example of _surfacescapes_' in use on the _Microsoft Surface Tabletop_@surfacescapes-images. The position of the models have been tracked by the system and outlined with a green cricle.])
)

_Foundry Virtual Tabletop_ @foundry is an application used to create fully digital _Dungeons and Dragons_ tabletops. These can either be used for remote play or in person play using a horizontal TV as a game board. _Foundry VTT_ allows for the creation of modules to add new functionality to your virtual tabletop. One such module is the _Material Plane_ @material-plane module which allows the tracking of physical miniatures on a TV game board. This functions by placing each miniature on a base containing an IR LED with an IR sensor then placed above the board. This can be configured to either move the closest "virtual" model to where the IR LED is or (with some internal electronics in the bases) can be set up to flash the IR LED in a pattern to attach different bases to specific models. An indicator LED is present to show when the IR LED is active.

#figure(
    image("images/foundry.jpg",width:60%),
    caption:([An example of  one of the _Material Plane_ bases. A miniature would be attached to the top. @material-plane-github.])
)

== Object Detection and Tracking Technologies

Finding a method to detect and find the positions of miniatures on a game board, whilst not obstructing the game, is the main focus of this project. This section will outline the different technological approaches that could be taken to achieve this.

=== RFID

An RFID approach is the somewhat obvious solution. This would involve embedding RFID chips underneath the bases of the miniatures. Then some method of reading these chips would then need to be embedded either within or underneath the game board. There are a number of different approaches that could be taken to locating RFID chips which have been outlined by Steve Hinske and Marc Langheinrich @rfid-based in their work on a similar project.

RFID solutions would require either an antenna grid underneath the game board or multiple individual RFID readers. This would be a viable option as hiding an antenna grid below a board is a relatively simple and unobstructive task. The same goes for hiding RFID readers beneath a table.

The main drawback of RFID is that a reader (at its core) can only detect if a chip is in range or not (referred to as "absence and presence" results). Due to this, some extra methodology would need to be implemented to determine the position of a chip.

One approach utilises increasing the range of an RFID reader to its maximum and then subsequently reducing the range repeatedly. Using the known ranges of the readers it would be possible to deduce which tags are within range of which reader - and subsequently deduce from which ranges it is detectable in the position of the RFID chip. This approach could in theory provide a reasonably accurate position of the RFID chip. However, this approach would take a longtime to update as each RFID reader would need to perform several read cycles. Combined with problems caused from interference between the chips / readers, the fact that being able to vary the signal strength of an RFID reader is not a common feature and the need for multiple RFID readers, this approach does not meet the requirements for this project.

Another approach utilises measuring the signal strength received from an RFID chip and estimating the distance from the reader to the chip, known as received signal strength indication (RSSI) . This approach is much quicker than the previous method needing only a single read cycle to determine distance. Most modern day RFID readers can report RF phase upon tag reading. However, current RSSI methods have an error range of \~60cm caused by noise data, false positives / negatives and NLOS (non-line of sight) @RSSI. This won't work for this project given than the board size is 70 x 60 cm.

Triliteration is a process in which multiple receivers use the time of arrival signal from a tag to determine it's position. This suffers from similar problems to other RFID methods in that it produces an area in which the tag could exist within - as opposed to it's exact position. Combined with the need for 3 RFID readers, this approach fails to be accessible to the target audience.

The approach previously mentioned in Steve Hinske and Marc Langheinrich's paper, which utilised an antenna grid below the game board, seemed promising. 

#figure(
    image("images/rfidCircle.png",width:60%),
    caption:([An example from Steve Hinske and Marc Langheinrich's paper @rfid-based describing their overlapping approach. The black square represents the RFID tag whilst the grey circles show the read area of each RFID reader. The intent is to use which readers are in range of the tag to determine an "area of uncertainty" of the tag's location.])
)

They were attempting to do this for _Warhammer 40k_, a game played on a much bigger board typically with larger models. As a result they were able to put RFID tags across larger models, such as vehicles, and utilise the known position of each tag relative to the model and the estimated position from the RFID readers to determine not only an accurate position but also orientation. Unfortunately for this project the size of the miniatures in _Kill Team_ would require the use of one tag or two in very close proximity. 

A potentially valid method utilizing RFID could be to use the approach outlined by Zhongqin Wang, Ning Ye, Reza Malekian, Fu Xiao, and Ruchuan Wan in their paper @rfid-tracking using first-order taylor series approximation to achieve mm level accuracy called _TrackT_. However, this approach is highly complex and can only track a small amount of tags at a time.

// READ THIS AND EXPLAIN

=== Machine / Deep Learning

// - YOLO?
// - Lots of different ML approaches
// - Size of dataset must be big
// - Problems with identifying specific minitures
// - Problematic when minitures will have similar paint schemes and poses - could be solved by looking at last known positions?
// - Difficulty in keeping objects "unique"

#todo("This should probably be improved upon - either by reading into deeplearning occlusion methods or recgonition methods of similar but different objects.")

Modern object tracking systems are often based on a machine learning or deep learning approach. In this case a classifier model would be used to identify each unique miniature on a team, and then subsequently locate it within the game board. The biggest drawback to this approach is the amount of training data needed for each class in a classifier. According to _Darknet's_ documentation (a framework for neural-networks such as YOLO) @yolo each class should have ~2000 training images.

Since each user will use their own miniatures, posed and painted in their own way, they would have to create their own dataset for their miniatures and train the model on them each time. As a user's miniatures are likely to follow a similar paint scheme, ML classification could potentially struggle to identify between miniatures from top down and far away if not enough training data is supplied.


=== ARKit

_Apple's_ ARKit supports the scanning and detection of 3D objects @ARKit by finding 3D spatial features on a target. Currently any phone running IOS 12 or above is capable of utilising the ARKit. In this system, you could scan in your models, then use the ARKit to detect them from above. This information could then be conveyed to the main system. This could also allow for the system to be expanded in the future to use a side on camera as opposed to just top down detection, allowing for verticality within other _Kill Team_ game systems. Combined with certain Apple products having an inbuilt LIDAR sensor (such as the _iPhone 12+ Pro_ and _iPad Pro_ 2020 - 2022), which further enhances the ARKit's detection, this could be a viable approach.

#figure(
    image("images/LIDAR.png", width:80%),
    caption:([Registering an an object in ARKit @ARKit])
)

After some testing utilizing an iPad Pro with a LIDAR scanner, some drawbacks were found with this approach. The object detection required you to be too close to the models detect them, and when being removed and re-added ARKit either took a long time to re-locate a model or failed to do so at all.

As a result I won't be using this approach for the project. Although, for future work, this could be an interesting option to explore allowing you to implement AR features such as highlighting models on your phone or tablet or displaying information above the model.

=== Computer Vision without neural networks

After considering all the options above, the best method found was using computer vision techniques.

One technique is blob detection. A blob is defined as a group of bright or dark pixels contrasting against a background. In this case the miniatures would be the blobs.

Utilizing blob analysis would allow locating general position of miniatures (as they would very clearly stick out from the background) but getting their exact center may then prove difficult (which would be needed for calculating movement and line of sight). Combined with the addition of terrain adding clutter to the image and the miniatures potentially being any colour, this approach could prove difficult to implement in the given time frame.

The computer vision method explored the most was utilizing coloured tags to identify miniatures.

The use of coloured tags would also mean there would be access to specific measurements allowing for an accurate location to be discerned. However, some external modification to the the game board or miniatures would need to be made. The challenge here is finding a way to do this without obstructing the flow of the game or the models themselves.

#todo("Actually talk about OpenCV")

== Computer Vision

#todo("Write up the papers on computer vision that were used.")

=== Fiducial Markers and Tag Detection

=== Occlusion solutions

=== Object Detection

=== Parallax Solutions

=== Calibration Solutions


// _STARS_ @STARS

// _TARboard_

// _UltraSound_

// Some of the systems previously mentioned use electronics embedded within the gameboard or within the game pieces to detect the position of minitures. As a result the average person would need specific hardware to use these systems.

= Project Description

This project aims to create a system that can track tabletop miniatures, in a game of _Kill Team Gallowdark_, using only materials easily accessible to the average miniature war-gamer. Then, utilise this system to create a digital representation of the game board. This digital representation will then be used to implement a few select game rules to demonstrate the system's capabilities and show that the tracking system provides the necessary information to process said rules.

The project can be broken down into two main goals.

#set enum(numbering: "1.a.")
+ Detection of the models and terrain to create a virtual representation of the game board.
    + The position of the miniature must be tracked accurately.
    + Be able to identify between different miniatures.
    + Aim to be non-invasive to the miniatures.
    + Be ambivalent to a model's shape and colour.
    + Be able to complete this task whilst being accessible to the average miniature war-gamer. Not utilising any equipment the average wargamer would not have access to in their own home.
+ Implementing the game logic in the virtual board to guide players through the game.
    + Allow users to select a model and which action they wish to preview.
    + Calculate the distance a model can move and display this on the virtual board.
      + Account for terrain that blocks movement.
    + Calculate the line of sight between the selected model and opposing models then display this on the virtual board.
      + Account for terrain that blocks line of sight.
      + Display the reasoning behind the line of sight calculation.
      + Display whether the target is obscured or in cover.
    + Display information about the selected model's odds to hit a target.

The methodology chosen to achieve these goals must meet the takeaways from the project background section. These requirements are not included here as they are more implementation specific instead of outlining the functionality of the project.


#todo("I'm not entirely sure if this meets the aims of setting up the requirements. A large portion of this project was spent on researching the best methodology to actually use, so going in depth here on the specifics of implementation feels wrong.")


#pagebreak()
= Methodology and Design

== Tracking Methodology

We settled on using a computer vision and tag based approach to detect the models and terrain. This would utilise placing a camera above the center of the gameboard on an adjustable stand and using tags to locate the models and terrain.

This approach was chosen for a few key reasons. Firstly, it is the most accessible option to the target audience. The only components needed are a camera, a computer, a printer and some method to position a camera above a board. Unlike RFID, IR or custom table methods, the average war-gamer would have access to these components. 

Secondly, it is the most flexible option. A tag based system does not care about the shape or colour of the models, only the tags. This requirement meant that machine learning approaches would not be as viable as the potential variation in models used is too high. If we stuck to only supporting specific, unmodified models this may potentially work, but this would place a restriction on the target audience and in a subject such as miniature wargaming where customisation is so heavily valued, this would not be a good approach. As well as this given the unique paint schemes each player may use this would mean an ML model would need to be either trained specifically for each players kill team or be able to use a models silhouette to identify it. Both of these approaches either require users to make their own datasets and train the model themselves, a time consuming and technical task, or require a model that can identify a model from its silhouette, a complex task that would require a lot of training data and wouldn't be that accurate due to potential model customisations #footnote("On a personal note, ai is not an area that I have much interest in and something which is, at the time of writing, currently all the craze. So doing something a bit different to the 'obvious' approach seemed interesting.").

#todo("Some images demonstrating the same model with different paint schemes")

Building on this, maintaining a unique identification for an object is a key requirement but is difficult to implement using a machine learning approach. Kill Team's can utilise multiple of the same type of operative, as a result the system would need to be able to track each "unique" operative despite having the same appearance. This becomes problematic when occlusion is introduced. If we were to move an operative and at the same time cover or move another operative of the same type, it would be difficult to differentiate which one was which. A potential solution would be to utilise similar technology to facial recognition models, particularly looking at research into identifying the differences between identical twins.

In contrast, a tag based system is ambivalent to the appearance of the model. This means the system is functional with any model, regardless of customisation which meets one of the main requirements of the project.

#todo("Actually put the citation in for this")


#todo("Unsure if the footnote here is too informal.")

Finally, a tag based system will assist with accuracy. Getting the location and rotation of an aurco tag using pose estimation is a well documented process. This methodology can be applied to a tag design that will function well with miniatures and terrain.

#todo("Grab some citation for 'well documented process'")


This project will use openCV @openCV to process the video feed from the camera. This library contains great support for computer vision tasks and is available for both Python and C++. An alternative image processing suite would be _MATLAB_ but this is not directly compatible with other languages so would require a lot of extra work to integrate with a visualisation system.

Python was chosen as the language for this project due to both prior knowledge and Python's loose type system contributing to the ability to produce quick working prototypes separate from the main project. C++ on the other hand would produce a more robust final product but would take longer to develop. As this project aims to serve as a proof of concept for the idea, Python fits the role better.



=== Camera Setup

A camera will have a view of the entire game board but will be distorted by two factors: Camera distortion and image distortion.


#todo("Get an image of the camera setup over the gameboard - or is that better to go in implementation?")

Camera distortion is caused by different camera designs having slightly different distortion in the images they produce due to the different lenses. This can be corrected by using a camera calibration method to produce a camera matrix and distortion coefficients which can be used to un-distort resultant images. Radial distortions result in the image having straight lines appear curved. Tangential distortions result in the image appearing tilted along an axis. OpenCv provides a simple method to calibrate a camera using a chessboard pattern. This produces the camera matrix and distortion coefficients which can be saved and used to un-distort images. It is important to note that each different camera will have a different distortion so will need to be calibrated separately.


#todo("Image showing camera distortion from the openCV docs")



Image distortion is caused by the actual location of the camera relative to the board. To correct this we can perform perspective correction. Taking a top down view of the board will not garuntee that the board will be rectangular in the image. For example, it is likey for the camera to not be perfectly level resulting in parts of the board appearing closer or longer than they actually are. To remedy this we can identify the four corners of the board and perform a perspective correction algorithm to produce a flattened version of the board. At the same time this will give us the boundaries of the board and crop the image.

#todo("Once again put an image in showing how this actually works - at the same time should probably cover aruco markers earlier")

The board corners will be located with aruco tags @arucoTags placed on the four corners.



#todo("Whilst this project is using a half sized board to simplify the problem it is important to note how a full sized board would be handled. Throw in an image to show how two cameras help with parallax - might just leave this out as it's not something I got round to doing.")


#figure(
  grid(
    columns: 2,
    image("images/perspectiveCorrection1.png",width:80%),
     image("images/perspectiveCorrection0.png",width:80%),
  ),
  caption: [An example of perspective correction in #cite(<whiteboard-scanning>,form: "prose")]
)



=== Terrain Detection

Terrain detection utilises a straightforward approach. As the shape of terrain is limited in _Kill Team Gallowdark_ to different constructions of pillar and wall. We can define a 2D model in the program to draw the terrain on the board. This means to detect terrain we only need to find a reference point to draw the model from, as opposed to needing to find the exact shape of the terrain. 

This is achieved using aruco tags. As previously mentioned these allow us to perform pose estimation to find the location and rotation of the tag relative to the camera. Each type of terrain is defined by a unique aruco tag in a range. For example, pillar with one wall can sit in the id range 1-10, pillar with two walls in the id range 11-20 etc. Once we have identified the rotation, translation and scale of the tag we can apply these transformations to the model to draw the terrain on the board.


=== Operative Detection and Identification

Operative detection is more complicated. Unlike terrain we can't place aruco tags on top of models as this is obstructive to the game and would appear signficantly out of place. Instead we will design a tag to be placed around the base of the model.

The tag must be able to provide two pieces of information: the position of the operative and which operative it is.

==== Position

As the models are placed on top of circular bases the position of the operative can be defined by the center point of the circle and the radius of it's base. As the base size of a model is set, and the board size is also known, we do not have to worry about finding the radius of the base. 

The requirements for the tag to provide the position are as such:

+ Be unobstructive to the model.
+ Be easily producable.
+ Be easily findable by the camera.
+ Provide the center point of the operatives base.
+ Achieve all of the above whilst also being able to be occluded by both terrain and the model itself.
  + Ideally the center point should be able to be found even with a quarter of the tag being visible.

These requirements resulted in this tag design:

#figure(
    image("images/circleYellow.jpg",width:50%,),
    caption: ([An example of the basic contrasting rim design.])
)

To achieve this a high contrast rim will be placed around the base of the model. In this implemention we have chosen to use a bright yellow #footnote("Although this could be changed to any colour which strongly contrasts the game board provided the correct thresholds were provided."). 

Utilising hough circle transforms @hough-circles in openCV we can easily find the center point of a provided circle. The "completeness" of the circle required to be determed as a ful circle can be easily adjusted to allow for occlusion.

Before we can attempt to locate the center point of the circle we need to clear the image of noise. This is done by bluring the image#footnote("This is done to help reduce other noise from the image and soften edges."), converting to HSV and then applying a threshold to only show the yellow colour space in the image. This leaves us with a binary image leaving only the yellow in the image.

#todo("Include images showing each step in this processing pipeline")

From here we perform edge detection on the image to find the edges of the circles in the image. This is done as hough circle detection is a very computationally expensive process and by finding the edges of the circles first we are left with a wireframe of the circles which reduces the space the hough circle detection needs to search.

This leaves our processing pipeline as such:

+ Apply a gaussian blur to the image
+ Convert the image to HSV
+ Apply a threshold to only show the yellow colour space
+ Apply edge detection to the image
+ Apply hough circle detection to the image

It is important to note that hough circle detection can easily mistake two close but separate circles as one circle.

#todo("A description of how HSV space works and why it's used here would be very useful")

#figure(
    image("images/detection.png",width:80%),
    caption: ([Circle detection on a gameboard with example terrain.])
)

In extreme cases where the rim is heavily blocked by terrain the system will be unable to locate the model. However due to the nature of this project being aimed at following the _Kill Team Gallowdark_ rule set, the terrain pieces used are placed along a grid. This prevents a situation where a terrain piece is very close to the edge of a board with a miniature placed behind resulting in the miniature being blocked from view. 


==== Identification

== Game Board Representation

Parallax is a problem that still needs to be addressed. Through testing it was found that using a standard game board size, the parallax was too great to expect to locate a rim. As a result, we have settled on using a two camera solution. This solves the parallax problem by having each camera watch a different half of the game board.

However, one problem with this approach is that calibration will be needed to ensure that the overlap between the cameras does not cause issues. This could be achieved by either calibrating the cameras to the game board, as it will be of a known size, by placing tags on each corner of the board. Alternatively the middle of the board could be marked with a piece of tape, or tags on the edges. This should then allow for the two images to be stitched together accurately.


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

Another rim will be placed around the bright contrast rim from before. This rim will be split into 6 sections. The first section will indicate the starting of the encoding and will use a unique colour. The other 5 sections will use 2 different colours to represent 1 or 0. Once a rim has been located, the system will then determine the orientation of the encoding circle. As the size is known, we can then rotate around the image of the encoding circle reading each section to eventually get a binary number. Each binary number will then represent a unique model on the board.

#figure(
    image("images/circle.png",width:60%),
    caption: ([An example of what the encoding circle could look like. The red section indicates the start of the encoding. The system would be able to determine which direction to read in based on the start encoding section being in the bottom or top half of the image.])
)

Another encoding method that was considered was to use one rim for both detection and identification. By using one rim of known colours, the image could be split into 3 images each containing only the colour of each segment. Each image would then be converted to black and white and recombined to create a singular image with the segments connected to create a full circle. After circle detection has been performed the system could then do the normal encoding reading. This approach would allow the rims of the miniatures to be significantly smaller and only require three contrasting colours.

One problem faced by this approach is that vision of the entire circle is needed to read the encoding, as a result if it is partially obscured then the system will be unable to identify the model.

This could be counteracted by splitting the encoding into quarters around the rim, so that as long as 1/4 of the encoding is visible, the system can correctly identify it. We can also exploit _Kill Team_ being a turn based game and simply compare the current game state with the previous game state to identify which pieces have been moved. A combination of active tracking and being able to determine which piece has moved, should allow for a robust system.

Terrain detection will be performed using two possible solutions, the user can either select predetermined terrain set ups or the system can detect the terrain pieces.

The current approach for terrain detection is to use QR codes on the top of each terrain piece. In _Gallowdark_ the size and shape of each terrain "module" is already known. As a result, the QR code can be used to determine the type of terrain and orientation. Then, since the terrain type has been established we already know the size and shape. So we can then fill it in on the virtual board.

Once the system has correctly identified and located each model and the terrain, a digital representation of the game board can be created.

#figure(
    image("images/board-suggestion.png"),
    caption: ([A proposed GUI for the game helper.])
) <GUI>

In @GUI the red semi-circle represents the valid area of movement for a selected operative. This can be calculated by splitting the game board into a very small grid, we can then apply a path finding algorithm (Dijkstra's, A\* etc) to the grid from the operative's starting point. We can then calculate all grid positions reachable by using a movement value less than or equal to the current operatives available movement characteristic.

Red circles around opposing operatives show they are in line of sight. This would be calculated using simple ray casting. A white and red circle indicates a selected opposing operative. This is to calculate the statistics on the right hand side of the screen to be specific to the opposing operative.

The information for the selected operative is displayed below the game board. A user can select the action they have performed / want to perform on the right hand side.

The GUI will be built in _PyQt_ @pyqt which is a python wrapper for the _Qt_ framework. One potential stretch goal is for the GUI and the detection system to be separate entities. For example, the detection system should be able to detect and track pieces without input needed from the virtual game board i.e. which model is selected. This would allow for other detection systems to be swapped out in the future or for other applications to be developed using the detection system.

= Implementation

== Camera Setup

=== Design and Calibration

=== Homography

== Model Detection

==== Colour Thresholding

=== Rim Detection

==== Hough Circles

=== Model Identification

=== Optimisations

== Terrain Detection

== Game Board Representation

=== Linking of Detected models and terrain to the virtual board

==== Operatives

=== Line of Sight

==== Obsucring and visible

==== Cover 


= Evaluation

= Summary and Reflections 

== Project Management

As per the initial Project Proposal the original goal for the first semester was to have ring detection and terrain detection completed. Currently, simple ring detection has been completed. This still needs to be expanded to include identification, though work has begun on this. Terrain detection has been moved backwards to allow for more time to make a good detection system for the miniatures.

Choosing to tackle the ring detection first was a good choice. This allowed for me to encounter larger issues and provide solutions to them whilst still in the research stages on the project. This has allowed for me to develop my computer vision skills and take approaches I would not have otherwise considered. For example, using a singular rim of multiple colours and combining the images to create a full circle for identification.

Supervisor meetings were held every week to check for blockers or advice on reports. Uniquely, our supervisor meetings were conducted as a group with the other two dissertation students my supervisor had. As all three of us were working on tabletop game based projects we were all knowledgeable in the area. This meant we could provide feedback or ideas for each others projects from a student perspective.

I found the Gantt chart to be unhelpful in managing the project. Gantt charts work well in well structured work environments. However, due to the nature of this semester having a large amount of other courseworks and commitments that needed to be balanced. An agile approach was much more effective, doing work when time was available. The nature of development work being much more effective when done in long, uninterrupted sessions meant that, with this semester's courseworks and lectures being very demanding at 70 credits, being able to find long swathes of uninterrupted time was very difficult between lectures, courseworks, tutorials etc. As a result, development was done in smaller, more frequent chunks which were not as effective as longer, less frequent chunks. I expect this to change next semester when the workload decreases down to 50 credits.

A much preferred method, that I will likely go ahead with, is Kanban. I personally found most use from the Gantt chart in that the project is naturally broken up into sub tasks. This approach of sub-tasking when,  combined with a less structured agile approach, is something that Kanban works really well at and have found effective in the past in GRP (COMP2002).

In the interests of being able to show current progress in comparison to previous I have included an updated Gantt chart (@firstGantt) along with the previous one (@secondGantt).

Looking at the time remaining I will focus on getting the main parts of the system functional. These are: model detection and tracking, terrain detection, virtual game board representation, movement preview and line of sight preview. If there is time available then I will aim to also implement the flow of the game (breaking it down into each phase, providing guidance of what to do in each phase, statistics etc). The most technically interesting part of this is the virtual game board and tracking technology. So placing a focus on having them work fluidly is more important to the dissertation.

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
      task("Dissertation", (11, 14), style: (stroke: 2pt + gray))
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
caption: ([The Updated Gantt chart])
) <firstGantt>
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
  caption: ([The original Gantt chart])
)<secondGantt>
] 

== Future Work and Reflections

Something I underestimated was the amount of time needed to research and determine which method should be used for model detection. A large amount of time was spent determining the viability of different approaches that may make the system more robust and easier to produce. As a result of this, development started later and took longer than was expected.

The biggest impact on this project was needing to get an extension on other coursework deadlines. This extension had a knock on effect of other courseworks which took priority over this project. The timings allotted in the Gantt chart did not take into account extensions being needed.

However, I am happy with the progress made so far. Having completed the methodology to find the circular tags even when partially obstructed is very promising to the viability of the chosen approach. As a result, I believe that a solid strategy has been chosen for model detection and identification and the work done so far has successfully laid a good foundation for the project.

=== Order Tokens and Objective Markers

=== Odds to Hit

=== Advanced Terrain

=== Height

=== Larger Game Board

=== Increasing the total number of operatives

=== Server Client Architecture For Game Board and Detection

=== Detection Upgrades
Hemming Distance

== LSEPI

The main LSEPI issue you could see here is copyright issues as _Kill Team_ is a copyrighted entity owned by _Games Workshop_. The way this project will handle this is by having the system implement the _Kill Team Lite_ rule set previously mentioned. This is publicly available published by _Games Workshop_. One issue is that different "_Kill Teams_" (groups of operatives) will have  different and unique rules as well as their own statistics pages. These are copyrighted and won't be able to be directly implemented. As a result of this, this project will implement basic operatives with fake statistic pages based off of the publicly published _Kill Team_ information. If this proves to be problematic then the game rules will be based off a very similar system _Firefight_ @one-page. This is published by _One Page Rules_, who produce free to use, public miniature war-game systems.

=== Accessability 


== Final Reflections

Official openCV python documentation is somewhat lacking.

=== Design Approach





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



