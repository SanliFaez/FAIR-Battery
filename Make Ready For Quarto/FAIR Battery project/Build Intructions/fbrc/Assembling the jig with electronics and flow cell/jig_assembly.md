---
Details:
    Thumbnail: images/Screenshot_20250102_190036.png
    Time: Tens of minutes
    Skills:
      - Mechanical assembly
---
<!-- There should be only one Header per page. You do not need to use all the keys -->
# Assembling the jig with electronics and flow cell

Gather the following components:
{{BOM}}

## Add reservoirs to jig {pagestep}

Insert the two [reservoirs](fromstep){qty: 2} into the [jig with pumps and power electronics](fromstep){qty: 1} as shown:


![](images/Screenshot_20250102_190203.png)

>!! **Warning** 
>!!
>!! One barb on each reservoir is slightly longer than the other barb. This longer barb is for electrolyte returning to the reservoir from the cell, and there is an internal channel in the reservoir that returns electrolyte to the top of the reservoir.
>!!
>!!The short barb is for electrolyte going to the pumps from the reservoir, and it draws electrolyte from the bottom of the reservoir. 
>!!
>!!![](images/Screenshot_20250102_190750.png)

## Add cell to jig and connect to tubing {pagestep}

Take the [assembled flow cell](fromstep){qty:1} and place it into the jig, connecting the tubing as described and shown:

Take the rest of the [cut tubing](fromstep){qty: 2,cat: part} and connect the lengths as so, for both positive and negative half-cells:
- pump outlet to inlet of cell (on bottom)
- outlet of cell (on top) to long barb on reservoir
- short barb on reservoir to pump inlet

![Same tubing principles apply for peristaltic pumps](images/front.png)



>!! **Warning** 
>!!
>!! Avoid creating kinks and sharp bends in the tubing when assembling the cell. This can create issues with electrolyte flow.



>!! **Warning** 
>!!
>!! Electrolyte flow must flow from bottom of the cell upwards to top, in order to clear out gas bubbles from the cell and ensure good liquid electrolyte flow

This makes an [assembled test jig]{output, qty: 1}.

