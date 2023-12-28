// I got this font from Google Fonts, you'll need to install it on your system
#set text(font: "EB Garamond", size: 11pt)

// Vertical space before
// needs to have:
// Project Title
// Name
// ID
// email
// name of the programme of your study
// project module
// 
#let diss-title(
    title: "Your Diss Title Goes Here",
    author:"Your Name",
    ID: "20363169",
    email: "psynb7",
    programme: "BSc Computer Science",
    module: "COMP3003",
    abstract: none,
    body,

) = {
    align(center)[
        #text(size: 18pt)[*Interim Report: #title*] \
        #text(size: 14pt)[#module]\
        #text(size: 14pt)[#author #email #ID]\
        #text(size: 14pt, style: "italic")[#programme]\  
    ]
    body
}


