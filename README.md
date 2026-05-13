# Seth Mini Data Warehouse — Jupyter Rebuild

This is a runnable reconstruction of the visible code from Seth's Jupyter screenshots.

## Run quick preview

```bash
pip install -r requirements_preview_only.txt
python -m streamlit run app.py
```

## Run the chart script

```bash
pip install -r requirements.txt
python src/visualizations.py
```

## Run the notebook

```bash
jupyter notebook
```

Open:

```txt
notebooks/visualizations_rebuilt.ipynb
```

## Security note

The screenshot showed a PostgreSQL password in the notebook. It has not been copied here.
Use `.env.example` and set your own `DATABASE_URL`.