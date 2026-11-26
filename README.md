# GPS trajectory reconstruction

Statistical evidence for *What GPS Trajectory Reconstruction Can Improve: Error Limits, Output Accuracy and Reuse* by Robin von Känel and Murat Sariyar.

The study evaluates distance and time in geographic areas from incomplete GPS observations. The coordinates supplied to an interpolator impose a lower bound on distance error when the path must preserve those coordinates.

## Check the reported results

Run the statistical replay with Python 3.12:

```sh
python -m pip install -r requirements.txt
python replay.py
```

The replay recomputes the GeoLife comparisons, grid-width intervals and group-weighted distance-floor summaries from group-level values. The `evidence/` directory also includes the reported aggregate contrasts for vehicle, smartphone and conditional diffusion experiments. `distance_error_floor.py` is the implementation of the per-window bound for supplied observations.

## Data sources and scope

The public files contain aggregated losses and contrasts. The GeoLife group labels are local to this package. Individual window manifests, source file names, exact start times, raw trajectories and model weights are omitted. The replay starts from group summaries and covers the statistical analysis described above. Window extraction, model fitting and scoring of raw provider files are outside its scope.

The original recordings are available from the [GeoLife provider](https://www.microsoft.com/en-us/download/details.aspx?id=52367), the [Vehicle Energy Dataset reference](https://doi.org/10.1109/TITS.2020.3035596), the [Safety Pilot Model Deployment catalog](https://catalog.data.gov/dataset/safety-pilot-model-deployment-data-fde1f), and the [Google Smartphone Decimeter Challenge](https://www.kaggle.com/competitions/smartphone-decimeter-2023/data) and [Suzuki navigation archive](https://github.com/taroz/gsdc2023). Provider terms apply to those recordings.
