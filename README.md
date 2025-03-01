# Data Cleaning in Python Essential Training
This is the repository for the LinkedIn Learning course Data Cleaning in Python Essential Training. The full course is available from [LinkedIn Learning][lil-course-url].

![1667582799961](https://user-images.githubusercontent.com/28540243/200747823-e4b24a18-e1ae-4075-bb04-02e4b8cd9da3.jpeg)

If you’re looking for more efficient ways to prepare your data for analysis, it’s time to level up your skill set and reassess your approach to data cleaning. In this course, instructor Miki Tebeka shows you some of the most important features of productive data cleaning and acquisition, with practical coding examples using Python to test your skills. Learn about the organizational value of clean high-quality data, developing your ability to recognize common errors and quickly fix them as you go. Along the way, Miki offers cleaning strategies that can help optimize your workflow, including tips for causal analysis and easy-to-use tools for error prevention.<br><br>This course is integrated with GitHub Codespaces, an instant cloud developer environment that offers all the functionality of your favorite IDE without the need for any local machine setup. With GitHub Codespaces, you can get hands-on practice from any machine, at any time—all while using a tool that you’ll likely encounter in the workplace. Check out the [Using GitHub Codespaces with this course][gcs-video-url] video to learn how to get started.

### Instructor

Miki Tebeka

Check out my other courses on [LinkedIn Learning](https://www.linkedin.com/learning/instructors/miki-tebeka?u=104).

[lil-course-url]: https://www.linkedin.com/learning/data-cleaning-in-python-essential-training-17061364
[lil-thumbnail-url]: https://media.licdn.com/dms/image/D560DAQG16fbd1_fa8w/learning-public-crop_675_1200/0/1667582799961?e=1668438000&v=beta&t=wG4qKGD3CPgQCIjuYQO0LDhzg-mAPknzJD95dhVeiEg
[gcs-video-url]: https://www.linkedin.com/learning/data-cleaning-in-python-essential-training-17061364/using-github-codespaces-with-this-course

---

# Notes

## Error in Data

1. Missing data
2. Extreme data (Out of scale)
3. Duplicate data

Chapter 1
```
df.dtypes
df[df.isnull().any(axis=1)]
df['amount'].astype('Int32')
```

```
df.sample(10)
df.groupby('name').describe()
df['name'].value_counts()
pd.pivot(df, index='time', columns='name').plot(subplots=True)
df.query('name == "cpu" & (value < 0 | value > 100)')


// remove outliers
mem = df[df['name'] == 'mem']['value']
z_score = (mem - mem.mean())/mem.std()
bad_mem = mem[z_score.abs() > 2]
df.loc[bad_mem.index]
```

```
df.duplicated(['date', 'name']) // find duplicated in date and name
```

```
df[df.isnull().any(axis=1)]
```

```
mask = df['name'].str.strip() == ''
df.loc[mask, 'name'] = np.nan
```


```
df = pd.read_csv('ships.csv')
df
# %%
import pandera as pa
import numpy as np

schema = pa.DataFrameSchema({
    'name': pa.Column(pa.String),
    'lat': pa.Column(
        pa.Float,
        nullable=True,
        checks=pa.Check(
            lambda v: v >= -90 and v <= 90,
            element_wise=True,
        ),
    ),
    'lng': pa.Column(
        pa.Float,
        nullable=True,
        checks=pa.Check(
            lambda v: v >= -180 and v <= 180,
            element_wise=True,
        ),
    ),
})

schema.validate(df)
```


### Apache Parquet
1. binary format with types and schema
2. to use parquet with pandas need apache arrow package (pyarrow)

```
size = 5
df = pd.DataFrame({
    'time': pd.date_range('2021', freq='17s', periods=size),
    'name': ['cpu'] * size,
    'value': np.random.rand(size) * 40,
})

import pyarrow as pa

schema = pa.schema([
    ('time', pa.timestamp('ms')),
    ('name', pa.string()),
    ('value', pa.float64()),
])

out_file = 'metrics.parquet'
df.to_parquet(out_file, schema=schema)

pd.read_parquet(out_file)
```