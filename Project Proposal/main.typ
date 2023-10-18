#import "template.typ": *

#set page(numbering: "1",number-align: center)
#show: diss-title.with(
    title: "Mixed Reality Tabletop War Game Assistant",
    author: "Nathan Burgess",
    ID: "20363169",
    email: "psynb7",
    programme: "BSc Computer Science",
    module: "COMP3003",
)

// wargaming and 

// wargaming
// OpenCV
// Computer Vision
// Mixed Reality
// Kill Team 


// Add page numbers to footer

// Number all headings
#set heading(numbering: "1.1")

// Tweak space above and below headings
#show heading: set block(above: 2em, below: 1.3em)

// Justified paragraphs
#set par(justify: true)

// Table of contents and start the rest of the stuff on a new page
// #outline()
// #pagebreak()

//Briefly describe the background to the projecet, importance/need and motivation for carrying out the work
// Explain the problem being solved and why

= Motivation and Background
// blah blah blah
== Introduction
Tabletop Wargaming is a popular hobby but, with a high barrier to entry, it remains niche and inaccessible to many. The rules to tabletop wargames can be complex and difficult to learn. This can be daunting for new players putting them off the hobby as well as causing arguments between seasoned players over different rules interpretations.

The most popular wargaming systems are produced by _Games Workshop_ #cite("gw-size"). One of their more popular systems, _Warhammer 40k_, has a core rulebook of 60 pages #cite("40k-rules") and the simplified version of another game system, _Kill Team_, is a rather dense three page spread #cite("kt-lite-rules").

Video games help on-board new players by having the rules of the game enforced by the game itself. This project aims to bring this experience to tabletop wargaming, specifically the _Kill Team Lite_ #cite("kt-lite-rules")  system. This is because the _Kill Team Lite_ rules are publically available from _Games Workshop's_ website and it is designed to be played on a smaller scale to other wargames, making it a good candidate for a proof of concept.

== Relevent Past Work

Previous attempts at digitising the state of a tabletop wargame have been made utilising RFID tags on models with an antenna grid beneath the table to triangulate the position of each tag #cite("rfid-based").

This approach works well to calculate the rough position of larger models with multiple RFID tags but smaller models with only one tag can prove difficult. This is because, using consumer grade electronics, finding the signal strength from an RFID tag to a receiver is often not supported or is inconsistent due to reflections, interference etc #cite("rfid-based"). As a result, the only information you can gather is whether a tag is in range of a receiver. Using this method with a single tag you can only find the rough area of a model by comparing the overlapping ranges of multiple recievers #cite("rfid-based").

== Project Overview

_Kill Team_, being a smaller scale game, only makes use of the smaller models. So an RFID approach would not be useful in tracking its exact location. This is needed to calculate the distance it can move and what other models are visible.

As a solution to this problem I want to use _OpenCV_ #cite("openCV") to interpret the state of the physical game board. Miniature models are typically placed on top of small, circular, black bases. To detect each model I plan to produce rings to go around these bases made of high contrast colours to allow a camera placed above the board to look for these rings and display the model's position on a top down virtual board.

Wargames often use terrain to provide cover for models. I plan to use pre-set terrain pieces where I have stored the corresponding dimensions of each piece. To detect these pieces of terrain I plan to put AR tags #cite("ar-tags") on the top of each piece. This would then allow me to accurately display the terrain on the virtual board and calculate the cover provided by each piece.

One downside of my approach is that calculating verticality within the game would be difficult to do. To solve this problem I plan to implement a gametype of _Kill Team Lite_ called _Gallowdark_. This terrain type is played on a flat board with no verticality.



// Aim: single sentence with a high level description of the project
// The aim of this project is to... develop / design / build 
// Objectives are the sub-components detailing individual aspects of the project

= Aims and Objectives

My aim in this project is to develop a system to produce a digital representation of a physical tabletop wargame. Then, using this representation, I aim to automate the rules of the game to provide a more accessible experience for players of all skill levels.

This project can be broken down into two main parts:

1. Vision Detection of the models and terrain to create a virtual representation of the game board.

2. Implementing the game logic in the virtual board to guide players through the game.

== Computer Vision

#set enum(numbering: "1.a)")
+ Detect the high contrast rings on the bases of the models to find the center point of the model.
  + Determine which ring belongs to which model.
+ Detect the AR tags on the terrain pieces.
+ Produce a top down view of the game board.
// Expected Issues
// Keeping game tokens in position 
== Game Logic

+ Allow users to select a model and a subsequent action (normal move, shoot, dash, capture objective).
+ Calculate the distance a model can move and display this on the virtual board.
  + Account for terrain that blocks movement.
+ Calculate the line of sight between the selected model and opposing models then display this on the virtual board.
  + Account for terrain that blocks line of sight.
+ Display information about the selected model's odds to hit a target.




// GANNT chart
// key dates, deliverables / milestomes, realistic - show other coursework times etc


// 1. Detecting high contrast rings with _openCV_. 2 weeks
// 2. Producing a visual game board with game objects with behaviour to move to different. locations and cast rays of a given length. 2 weeks
// 3. Detecting AR tags to correctly identify and orient a piece of terrain. 2 weeks
// 4. Displaying valid movement positions for a limited movement distance accounting for terrain. 3 weeks 
// 5. Ray casting from a points to detect other points,accounting for cover.2 weeks 
// 6. Game Flow 4 weeks

#pagebreak()
= Project Plan

The structure of this project plan aims to focus on the development of the computer vision aspect first. This is because this area is likely to be the most technically challenging. Completing this first allows me to focus on getting this correct before moving on to other parts of the project.

I have purposely been generous with the time allocated to some tasks. This is becuase they should provide a buffer for any unexpected issues that may arise, particularly with more technically complex aspects of the project.

This is especially apparent with other commitments. Due to the nature of courseworks not being fully released at the time of writing I am unable to make a more accurate guess of the time they will take to complete.

This project plan places most of the work to be done in the Spring semester due to it containing only 50 credits compared to 70 credits in the Autumn semester.

I have allocated time for my interim report to be earlier than the deadline due to other commitments having the same deadline that I would be more likely to prioritise over the interim report. This is also because I plan to produce the interim report somewhat iteratively, adding to it as I complete tasks. The same goes for the final dissertation.

// Bibliography
= Bibliography
#bibliography( title: none, "biblio.yml")



#page(flipped: true)[

  

#import "@preview/timeliney:0.0.1"

#timeliney.timeline(
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

    taskgroup(title: [*Development: Computer Vision*], {
      task("Ring Detection", (3, 5), style: (stroke: 2pt + gray))
      task("Terrain Detection", (5, 7), style: (stroke: 2pt + gray))
      task("Board Generation", (7, 8), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Development: Game Logic*], {
      task("Game Board Framework",(13.75,16), style: (stroke: 2pt + gray))
      task("Movement",(16,18), style: (stroke: 2pt + gray))
      task("Line of Sight",(18,19), style: (stroke: 2pt + gray))
      task("Game Flow",(19,22), style: (stroke: 2pt + gray))
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
)
]