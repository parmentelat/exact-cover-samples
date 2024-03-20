# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     formats: py:percent
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
# %matplotlib ipympl

# %% [markdown]
# # benchmarking

# %% [markdown]
# ## loading results

# %%
df = pd.read_csv("results.csv")
df.shape

# %%
df.head()

# %% [markdown]
# ## errors

# %%
df[df.computed == -1]

# %%
df[df.error.notna()]

# %% [markdown]
# ## keeping only run 1

# %%
df = df[df.run == 1]
df.shape

# %% [markdown]
# ## artificially divide exact-cover-py by 50

# %%
time_series = df.time
updated = time_series[df.library == "exact-cover-py"] / 50
time_series.update(updated)

library_series = df.library
updated = library_series[df.library == "exact-cover-py"]
updated[:] = "exact-cover-py / 50"
library_series.update(updated)

# %% [markdown]
# ## drawing

# %%
keep = "library+problem+requested+time".split("+")

table = df[keep].pivot_table(columns=["requested", "library"], index="problem", values="time")
table

# %%
df_all_solutions = table.loc[:, 0]
df_all_solutions.plot()
plt.savefig("results.svg", format="svg")
plt.savefig("results.png", format="png")
