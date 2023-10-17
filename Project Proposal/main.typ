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

Video games help on-board new players by having the rules of the game enforced by the game itself. This project aims to bring this experience to tabletop wargaming, specifically the _Kill Team lite_ #cite("kt-lite-rules")  system. This is because the _Kill Team Lite_ rules are publically available from _Games Workshop's_ website and it is designed to be played on a smaller scale to other wargames, making it a good candidate for a proof of concept.

== Relevent Past Work

Previous attempts at digitising the state of a tabletop wargame have been made utilising RFID tags on models with an antenna grid beneath the table to triangulate the position of each tag #cite("rfid-based").

This approach works well to calculate the rough position of larger models with multiple RFID tags but smaller models with only one tag can prove difficult. This is because, using consumer grade electronics, finding the signal strength from an RFID tag to a receiver is often not supported or is inconsistent due to reflections, interference etc #cite("rfid-based"). As a result, the only information you can gather is whether a tag is in range of a receiver. Using this method with a single tag you can only find the rough area of a model by comparing the overlapping ranges of multiple recievers #cite("rfid-based").

== Project Overview

_Kill Team_, being a smaller scale game, only makes use of the smaller models. So an RFID approach would not be useful in tracking it's exact location. This is needed to calculate the distance it can move and what other models are visible.

As a solution to this problem I want to use _OpenCV_ #cite("openCV") to interpret the state of the physical game board. Miniture models are typically placed on top of small, circular, black bases. To detect each model I plan to produce rings to go around these bases made of high contrast colours to allow a camera placed above the board to look for these rings and display the models position on a top down virtual board.

Wargames often use terrain to provide cover for models. I plan to use pre-set terrain pieces where I have stored the corresponding dimensions of each piece. To detect these pieces of terrain I plan to put AR tags #cite("ar-tags") on the top of each piece. This would then allow me to accurately display the terrain on the virtual board and calculate the cover provided by each piece.

One downside of my approach is that calculating verticality within the game would be difficult to do. To solve this problem I plan to implement a gametype of _Kill Team Lite_ called _Gallowdark_. This terrain type is played on a flat board with no verticality.


// Aim: single sentence with a high level description of the project
// The aim of this project is to... develop / design / build 
// Objectives are the sub-components detailing individual aspects of the project

= Aims and Objectives

My aim in this project is to develop a system to produce a digital representation of a physical tabletop wargame. Then, using this representation, I aim to automate the rules of the game to provide a more accessible experience for new players.
// GANNT chart
// key dates, deliverables / milestomes, realistic - show other coursework times etc
= Project Plan

// Bibliography
= Bibliography
#bibliography( title: none, "biblio.yml")



