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
      task("Graphics Coursework 1", (9,11.5), style: (stroke: 2pt + gray))
      task("Graphics Coursework 2", (11,19), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Initial Write-up*], {
      task("Interim Report", (0, 0.25), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Computer Vision*], {
      task("Multi Ring Tracking",(5,6),style: (stroke: 2pt + gray))
      task("Ring Identification", (8.5,12), style: (stroke: 2pt + gray))
      task("Terrain Detection", (14, 15), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Game Logic*], {
      task("Game Board Framework",(11.5,15.5), style: (stroke: 2pt + gray))
      task("Line of Sight",(13,14.5), style: (stroke: 2pt + gray))
    })

    taskgroup(title: [*Final Write-up*], {
      task("Dissertation", (14, 16), style: (stroke: 2pt + gray))
      task("Presentation Prep", (16, 18.5), style: (stroke: 2pt + gray))
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
      at: 16,
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
caption: ([The final Gantt chart, showing the work done.])
) <thirdGannt>
]

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
