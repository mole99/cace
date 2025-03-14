# Supported Tools

CACE supports a variety of EDA tools. See the entries below for a list of supported tools and their implemented functionality.

## `ngspice`

Perform spice simulation using ngspice.

Arguments:

- `template`: `<string>` The template schematic under the `templates/` folder for simulation.
- `collate`: `<string>` Used to collate results for Monte Carlo simulations.
- `format`: `<'ascii'>` The file format of the ngspice result. Currently only `ascii` is supported.
- `suffix`: `<string>` File extension of the result file. For example: `.data`.
- `variables`: `<List[string|null]>` A list of results inside the result file. Use `null` to ignore a column.
- `script` (optional): `<string>` Name of a Python script in the script folder. It will be executed on the results of each simulation.
- `script_variables` (optional): `<List[string|null]>` A list of results generated by the specified Python script. These results are available in addition to the ones specified under `variables`. TODO

Results: The results depend on the `variables` and optionally the `script_variables` arguments.

## `magic_drc`

Perform DRC (Design Rule Check) with magic.

Arguments:

- `args`: `<list[string]>` Additional args that are passed to magic.
- `gds_flatten`: `<true/false>` Flatten the GDSII layout prior to running DRC.

Results:

- `drc_errors`: `<int>` Number of DRC errors.

## `magic_area`

Perform area measurements with magic.

Arguments:

- `args`: `<list[string]>` Additional args that are passed to magic.

Results:

- `area`: `<float>` Area of the design in µm²
- `width`: `<float>` Width of the design in µm.
- `height`: `<float>` Height of the design in µm.

## `magic_antenna_check`

Perform the magic antenna check to find antenna violations in the layout.

Arguments:

- `args`: `<list[string]>` Additional args that are passed to magic.

Results:

- `antenna_violations`: `<int>` The number of antenna violations.

## `klayout_drc`

Perform DRC (Design Rule Check) with KLayout.

Arguments:

- `args`: `<list[string]>` Additional args that are passed to KLayout. For example `['-rd', 'feol=true']`.

Results:

- `drc_errors`: `<int>` Number of DRC errors.

## `netgen_lvs`

```{note}
The `netgen_lvs` tool always compares the `schematic` netlist with the `layout` extracted netlist, independent of the selected netlist source.
```

Perform LVS (Layout VS Schematic) with netgen.

Arguments:

- `args`: `<list[string]>` Additional args that are passed to netgen.
- `script`: `<string>` A custom LVS script under `scripts/`.

Results:

- `lvs_errors`: `<int>` Number of LVS errors.

## Missing a tool?

If you are missing a tool or functionality, please open an issue [here](https://github.com/efabless/cace/issues).
