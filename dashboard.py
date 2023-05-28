import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_daily_params_df(df):
    daily_params_df = df.resample(rule='D', on='date').agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    })
    daily_params_df = daily_params_df.reset_index()
    return daily_params_df


def create_hourly_params_df(df):
    hourly_params_df = df.groupby('hour_periods').agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "TEMP": "mean",
        "DEWP": "mean",
    })

    hourly_params_df.reset_index(inplace=True)
    return hourly_params_df


def create_windspeed_df(df):
    windspeed_df = df.groupby('windir').agg({
        "WSPM": "mean",
    })

    windspeed_df.reset_index(inplace=True)
    return windspeed_df


df_all = pd.read_csv("main_data.csv")
df_all.sort_values(by=["date", "hour"], inplace=True)
df_all.reset_index(inplace=True)
df_all["date"] = pd.to_datetime(df_all["date"])

min_date = df_all["date"].min()
max_date = df_all["date"].max()

with st.sidebar:

    st.image("https://i.ibb.co/wg8wF66/Screenshot-1.jpg")

    start_end_date = st.date_input(
        label='Time Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    try:
        start_date, end_date = start_end_date
    except ValueError:
        st.error("You must pick a start and end date")
        st.stop()

    genre = st.radio(
        label="Station",
        options=('All', 'Shunyi', 'Tiantan'),
        horizontal=False
    )

    if genre == 'All':
        # No filter
        filtered_df = df_all
    elif genre == 'Shunyi':
        # Filter to Shunyi station
        filtered_df = df_all[df_all["station"] == "Shunyi"]
    else:
        # Filter to Tiantan station
        filtered_df = df_all[df_all["station"] == "Tiantan"]

main_df = filtered_df[(filtered_df["date"] >= str(start_date)) &
                      (filtered_df["date"] <= str(end_date))]

daily_params_df = create_daily_params_df(main_df)
hourly_params_df = create_hourly_params_df(main_df)
windspeed_df = create_windspeed_df(main_df)


st.header('Station Air Quality Dashboard :earth_americas:')

st.subheader('Parameter Overview')

column_metrics1 = ["PM2.5", "SO2", "CO"]
columns1 = st.columns(len(column_metrics1))

for index, column in enumerate(column_metrics1):
    col = columns1[index]
    avg_column = round(daily_params_df[column].mean(), 2)
    col.metric(f"Avg {column}", value=avg_column)

column_metrics2 = ["PM10", "NO2", "O3"]
columns2 = st.columns(len(column_metrics2))

for index, column in enumerate(column_metrics2):
    col = columns2[index]
    avg_column = round(daily_params_df[column].mean(), 2)
    col.metric(f"Avg {column}", value=avg_column)

fig, ax = plt.subplots(2, 1, figsize=(18, 12))
ax[0].plot(
    daily_params_df["date"],
    daily_params_df[["PM2.5", "PM10"]],
    marker='o',
    linewidth=2,
)
ax[0].legend(["PM2.5", "PM10"], fontsize=22, loc="upper right")
ax[0].tick_params(axis='y', labelsize=18)
ax[0].tick_params(axis='x', labelsize=18)

ax[1].plot(
    daily_params_df["date"],
    daily_params_df[["SO2", "NO2"]],
    marker='x',
    linewidth=3,
)
ax[1].legend(["SO2", "NO2"], fontsize=22, loc="upper right")
ax[1].tick_params(axis='y', labelsize=18)
ax[1].tick_params(axis='x', labelsize=18)

st.pyplot(fig)


st.subheader('Average Hourly Monitor')
fig, ax = plt.subplots(2, 2, figsize=(20, 20))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="CO", x="hour_periods", data=hourly_params_df.sort_values(
    by="hour_periods", ascending=True), palette=colors, ax=ax[0, 0])
ax[0, 0].set_ylabel(None)
ax[0, 0].set_xlabel(None)
ax[0, 0].set_title("Carbon monoxide (CO)", fontsize=35)
ax[0, 0].tick_params(axis='y', labelsize=23)
ax[0, 0].tick_params(axis='x', labelsize=23, rotation=30)

sns.barplot(y="O3", x="hour_periods", data=hourly_params_df.sort_values(
    by="hour_periods", ascending=True), palette=colors, ax=ax[0, 1])
ax[0, 1].set_ylabel(None)
ax[0, 1].set_xlabel(None)
ax[0, 1].set_title("Ozon (O3)", fontsize=35)
ax[0, 1].tick_params(axis='y', labelsize=23)
ax[0, 1].tick_params(axis='x', labelsize=23, rotation=30)

sns.barplot(y="TEMP", x="hour_periods", data=hourly_params_df.sort_values(
    by="hour_periods", ascending=True), palette=colors, ax=ax[1, 0])
ax[1, 0].set_ylabel(None)
ax[1, 0].set_xlabel(None)
ax[1, 0].set_title("Temperature", fontsize=35)
ax[1, 0].tick_params(axis='y', labelsize=23)
ax[1, 0].tick_params(axis='x', labelsize=23, rotation=30)

sns.barplot(y="DEWP", x="hour_periods", data=hourly_params_df.sort_values(
    by="hour_periods", ascending=True), palette=colors, ax=ax[1, 1])
ax[1, 1].set_ylabel(None)
ax[1, 1].set_xlabel(None)
ax[1, 1].set_title("Dewpoint", fontsize=35)
ax[1, 1].tick_params(axis='y', labelsize=23)
ax[1, 1].tick_params(axis='x', labelsize=23, rotation=30)

plt.tight_layout()
plt.show()

st.pyplot(fig)

st.subheader("Wind Speed Preview")
col1, col2, col3 = st.columns(3)


with col1:
    max_wind = round(windspeed_df.WSPM.max(), 2)
    st.metric("Max Wind speed", value=f"{max_wind} m/s")

with col2:
    avg_wind = round(windspeed_df.WSPM.mean(), 2)
    st.metric("Avg Wind speed", value=f"{avg_wind} m/s")


with col3:
    min_wind = round(windspeed_df.WSPM.min(), 2)
    st.metric("Min Wind speed", value=f"{min_wind} m/s")


fig, ax = plt.subplots(1, 2, figsize=(20, 8))
colors = ["#90CAF9", "#90CAF9"]

sns.barplot(y="windir", x="WSPM", data=windspeed_df.sort_values(
    by="windir", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Avg wind speed (m/s)", fontsize=23)
ax[0].set_title("Strongest wind direction", fontsize=35)
ax[0].tick_params(axis='y', labelsize=23)
ax[0].tick_params(axis='x', labelsize=23)
ax[0].set_xlim(0, 3.2)

sns.barplot(y="windir", x="WSPM", data=windspeed_df.sort_values(
    by="windir", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Avg wind speed (m/s)", fontsize=23)
ax[1].set_title("Slowest wind direction", fontsize=35)
ax[1].tick_params(axis='y', labelsize=23)
ax[1].tick_params(axis='x', labelsize=23)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_xlim(3.2, 0)

st.pyplot(fig)
