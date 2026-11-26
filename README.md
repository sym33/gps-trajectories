# GPS trajectory reconstruction

Statistical evidence for *What GPS Trajectory Reconstruction Can Improve: Error Limits, Output Accuracy and Reuse* by Robin von Känel and Murat Sariyar.

The study evaluates distance and time in geographic areas from incomplete GPS observations. The coordinates supplied to an interpolator impose a lower bound on distance error when the path must preserve those coordinates.

## What the CSV files contain

The 17 public CSV files contain group-level values and contrasts. The original GeoLife analysis scores 277 one-hour windows from 14 people. Scoring the same windows across observation conditions, methods and targets produces 68,885 window-level loss rows.

| Analysis | Accompanying research archive | Public GitHub files |
| --- | ---: | ---: |
| GeoLife losses | 68,885 window-level loss rows | 3,523 group means |
| Distance-error floor | 6,748 window/reference/preprocessing rows | 2,656 group-level rows and 64 summaries |

The 36 rows in `evidence/geolife_grid_width_contrasts.csv` cover all 12 observation conditions at three grid widths. The public tables support statistical replay from group-level inputs. Inspection of individual window errors requires the separate archive accompanying the manuscript. Omitting the exact start times and source files from the public deposit reduces direct links to the provider trajectories.

## Check the reported results

Run the statistical replay with Python 3.12:

```sh
python -m pip install -r requirements.txt
python replay.py
```

The replay recomputes the GeoLife comparisons, grid-width intervals and group-weighted distance-floor summaries from group-level values. The `evidence/` directory also includes the reported aggregate contrasts for vehicle, smartphone and conditional diffusion experiments. `distance_error_floor.py` is the implementation of the per-window bound for supplied observations.

## Data sources and scope

The GeoLife group labels are local to this package. Window extraction, model fitting and scoring of provider files use the separate research archive and the original recordings.

The original recordings are available from the [GeoLife provider](https://www.microsoft.com/en-us/download/details.aspx?id=52367), the [Vehicle Energy Dataset reference](https://doi.org/10.1109/TITS.2020.3035596), the [Safety Pilot Model Deployment catalog](https://catalog.data.gov/dataset/safety-pilot-model-deployment-data-fde1f), and the [Google Smartphone Decimeter Challenge](https://www.kaggle.com/competitions/smartphone-decimeter-2023/data) and [Suzuki navigation archive](https://github.com/taroz/gsdc2023). Provider terms apply to those recordings.
