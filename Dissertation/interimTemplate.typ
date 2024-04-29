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
    programme: "BSc Hons Computer Science",
    module: "COMP3003",
    abstract: none,
    body,

) = {
    align(center)[
        #image("images/uonLogo.png", width:60%)
        #v(20pt)
        #text(size: 18pt)[*#title*] \
        #v(40pt)
        #text(size: 14pt)[Submitted April 2024, in partial fulfilment of 
        
        the conditions for the award of the degree:
        ]\
        #text(size: 14pt, style:"italic")[*#programme*]\
        #v(40pt)
        #text(size: 14pt)[#ID]\
        #text(size: 14pt)[School of Computer Science]\
        #text(size: 14pt)[University of Nottingham]\
        #v(40pt)
        #text(size: 14pt)[I hereby declare that this dissertation is all my own work, except as indicated in the text:]\

        #v(10pt)
        #text(size: 14pt)[Signature: NB ]\
        #text(size: 14pt)[Date: 13/04/24]\
        #v(40pt)
        #text(size: 14pt)[I hereby declare that I have all necessary rights and consents to publicly distribute this dissertation via the University of Nottingham's e-dissertation archive.\*]\
        
    ]
    set page(numbering: "i",number-align: center)
    body
}


