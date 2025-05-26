::::: site-header
:::: {.wrapper .header-wrapper}
::: header-text
# Building a benchtop flow battery test cell with a zinc-iodide electrolyte {#building-a-benchtop-flow-battery-test-cell-with-a-zinc-iodide-electrolyte .site-title}

by Kirk Pollard Smith and Daniel Fernandez Pinto

Flow Battery Research Collective
:::
::::
:::::

::::: page-content
<div>

[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTggMTUiPgogICAgICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiM0MjQyNDIiIGQ9Ik0xOCwxLjQ4NGMwLDAuODItMC42NjUsMS40ODQtMS40ODQsMS40ODRIMS40ODRDMC42NjUsMi45NjksMCwyLjMwNCwwLDEuNDg0bDAsMEMwLDAuNjY1LDAuNjY1LDAsMS40ODQsMCBoMTUuMDMxQzE3LjMzNSwwLDE4LDAuNjY1LDE4LDEuNDg0TDE4LDEuNDg0eiIgLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsPSIjNDI0MjQyIiBkPSJNMTgsNy41MTZDMTgsOC4zMzUsMTcuMzM1LDksMTYuNTE2LDlIMS40ODRDMC42NjUsOSwwLDguMzM1LDAsNy41MTZsMCwwYzAtMC44MiwwLjY2NS0xLjQ4NCwxLjQ4NC0xLjQ4NCBoMTUuMDMxQzE3LjMzNSw2LjAzMSwxOCw2LjY5NiwxOCw3LjUxNkwxOCw3LjUxNnoiIC8+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iIzQyNDI0MiIgZD0iTTE4LDEzLjUxNkMxOCwxNC4zMzUsMTcuMzM1LDE1LDE2LjUxNiwxNUgxLjQ4NEMwLjY2NSwxNSwwLDE0LjMzNSwwLDEzLjUxNmwwLDAgYzAtMC44MiwwLjY2NS0xLjQ4NCwxLjQ4NC0xLjQ4NGgxNS4wMzFDMTcuMzM1LDEyLjAzMSwxOCwxMi42OTYsMTgsMTMuNTE2TDE4LDEzLjUxNnoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](#){.menu-icon}

-   [Building a benchtop flow battery test cell with a zinc-iodide
    electrolyte](./){.navhome}

-   :::::: {#nav-search}
    ::::: {.search-results v-if="focused && searchTerm.length > 0"}
    ::: {v-if="searchResults.length > 0"}
    Results:
    :::

    ::: {v-if="searchResults.length === 0"}
    No results.
    :::

    [[ \${crumb + \' \> \'}
    ]{v-for="crumb in result.breadCrumbs.slice(0, -1)"} \${result.title
    \|\| result.breadCrumbs\[result.breadCrumbs.length -
    1\]}]{.search-result :href="`./${result.path}.html`"}
    [\${node.chars}]{v-for="node in result.highlightChars"
    :class="node.mark ? 'highlight' : ''"}
    :::::
    ::::::

-   [Bill of Materials](./index_BOM.html){.active}

-   [Fabricating components](./fabrication.html){.not-active}

-   [Preparing the pumps and power
    electronics](./electronics.html){.not-active}

-   [Assembling the flow cell from
    components](./cell_assembly.html){.not-active}

-   [Assembling the jig with electronics and flow
    cell](./jig_assembly.html){.not-active}

-   [Leak testing the cell](./leak_test.html){.not-active}

-   [Preparing the electrolyte](./electrolyte.html){.not-active}

-   [Operating and testing the cell](./testing.html){.not-active}

-   [Stopping and disassembling the cell](./cleanup.html){.not-active}

-   [Analyzing and storing the experimental
    data](./analysis.html){.not-active}

</div>

::: wrapper
# Bill of Materials

Download this as a [CSV file](index_BOM.csv)

### Parts

-   a small plate of [1 mm brass sheet](brass.html){.bom}
-   2 [19/22 silicone septa](septa.html){.bom}
-   1 [24 V DC power source](missing){.missing} - Anything between 12 V
    and 24 V may work but the results achieved here use 24 V. Motor
    speeds may need calibration to match existing results
-   1 [Arduino UNO R3](missing){.missing} - or equivalent
    microcontroller that can output two independent 5V PWM signals and
    connect to PC over USB serial
-   4 cm² of [conductive felt](conductive_felt.html){.bom}
-   160 cm² of [gasket sheet](gaskets.html){.bom} - Dimensions must be
    at least enough to cut out approx. four 6 cm x 8 cm rectangles, an
    A4 sheet is enough
-   100 cm² of [grafoil](grafoil.html){.bom}
-   1 [L298N motor driver](drivers.html){.bom}
-   4 [M6 nuts with washers](missing){.missing}
-   4 [M6 x 35 mm hex socket cap bolts with washers](missing){.missing}
-   several [male-to-male breadboard jumper cables](missing){.missing}
-   2 cm² of [nonconductive felt](nonconductive_felt.html){.bom}
-   2 [peristaltic pumps](missing){.missing}
-   some [polypropylene filament](missing){.missing} - This can be
    substituted if you only plan to run water through the cell for
    testing things other than the chemistry
-   several cm [polypropylene packing tape](missing){.missing}
-   A4 sheet [separator sheet](separator_sheet.html){.bom}
-   some [stiff filament](missing){.missing} - PLA works
-   44 cm of [tubing](tubing.html){.bom}
-   1 [USB A-to-B cable](missing){.missing}

### Tools

-   1 [10 mm socket](missing){.missing} - To fit torque wrench
-   1 [5 mL syringe](missing){.missing}
-   1 [50 mL beaker](missing){.missing}
-   2 [50 mL beakers](missing){.missing} - or drip tray/other container
    to hold 10 mL of water
-   1 [5mm hex key](missing){.missing}
-   1 [FDM printer](missing){.missing}
-   1 [gasket cutter machine](missing){.missing} - Vinyl/laser cutter or
    hand tools
-   1 [pair of chemical safety goggles](missing){.missing}
-   1 [pair of nitrile gloves](missing){.missing}
-   1 [PC](missing){.missing} - Must be able to flash firmware to
    microcontroller and connect over USB serial to microcontroller and
    potentiostat
-   1 [potentiostat](pstat.html){.bom} - preferably the MYSTAT
-   1 [scale](missing){.missing}
-   1 [stir bar](missing){.missing}
-   1 [stir plate](missing){.missing}
-   1 [torque wrench](missing){.missing} - to accept 5 mm allen key or
    10 mm hex socket
-   1 [utility knife](missing){.missing}
-   1 [vial](missing){.missing} - min. 20 mL
-   1 [weighing spatula](missing){.missing}

### Chemicals

-   10.0 grams of [8% vinegar/acetic acid](missing){.missing}
-   10 mL of [deionized water](missing){.missing}
-   3.0 grams of [potassium acetate](missing){.missing}
-   6.6 grams of [potassium iodide](missing){.missing}
-   2.8 grams of [zinc chloride](missing){.missing}

------------------------------------------------------------------------

[Previous page](index.html) \| [Next page](fabrication.html)
:::
:::::

::: wrapper
[![GitBuilding logo](./static/Logo/GitBuilding500x.png){.icon}
[Documentation powered by
GitBuilding]{.doc-info}](https://gitbuilding.io){target="_blank"
rel="noopener noreferrer"}

©2025 Kirk Pollard Smith and Daniel Fernandez Pinto

Contact: <info@fbrc.dev>

Building a benchtop flow battery test cell with a zinc-iodide
electrolyte is released under [CERN-OHL-S-2.0](license.html).
:::
