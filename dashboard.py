import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Café Behavioral Analytics", page_icon="☕", layout="wide")

FILE = "Cafe_Analysis_Performed.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(FILE, sheet_name=None)

try:
    data = load_data()
except FileNotFoundError:
    st.error(f"'{FILE}' was not found. Keep the Excel file in the same folder as dashboard.py.")
    st.stop()

def sheet(name):
    return data.get(name, pd.DataFrame())

happiness = sheet("Happiness")
engagement = sheet("Engagement")
adoption = sheet("Adoption")
retention = sheet("Retention")
task_success = sheet("Task Success")
customers = sheet("Customer_Visitor")
orders = sheet("Orders")

def nps_category(x):
    if pd.isna(x):
        return None
    if x <= 6:
        return "Detractor"
    if x <= 8:
        return "Passive"
    return "Promoter"

def nps_score(df):
    if "NPS Response" not in df:
        return None
    x = pd.to_numeric(df["NPS Response"], errors="coerce").dropna()
    if x.empty:
        return None
    c = x.apply(nps_category)
    return ((c == "Promoter").mean() - (c == "Detractor").mean()) * 100

def sus_score(df):
    cols = [f"SUS_Q{i}" for i in range(1, 11)]
    if not all(c in df.columns for c in cols):
        return None
    score = sum(pd.to_numeric(df[f"SUS_Q{i}"], errors="coerce") - 1 for i in range(1, 11, 2))
    score += sum(5 - pd.to_numeric(df[f"SUS_Q{i}"], errors="coerce") for i in range(2, 11, 2))
    return (score * 2.5).mean()

def ttfv_score(df):
    if not {"Signup Time", "First Value Time"}.issubset(df.columns):
        return None
    a = pd.to_datetime(df["Signup Time"], errors="coerce")
    b = pd.to_datetime(df["First Value Time"], errors="coerce")
    return ((b - a).dt.total_seconds() / 60).dropna().mean()

def task_error(df):
    if not {"Task Attempt Flag", "Error Count"}.issubset(df.columns):
        return None
    attempts = pd.to_numeric(df["Task Attempt Flag"], errors="coerce").sum()
    errors = pd.to_numeric(df["Error Count"], errors="coerce").sum()
    return errors / attempts * 100 if attempts else None

def task_completion(df):
    if not {"Session ID", "Status"}.issubset(df.columns):
        return None
    x = df.groupby("Session ID")["Status"].apply(lambda s: (s == "Success").any())
    return x.mean() * 100 if len(x) else None

def core_action(df):
    if not {"Session ID", "Action"}.issubset(df.columns):
        return None
    x = df.assign(Core=df["Action"].eq("Order Completed").astype(int))
    x = x.groupby("Session ID")["Core"].max()
    return x.mean() * 100 if len(x) else None

def day7(df):
    if "Day7_Return" not in df:
        return None
    x = pd.to_numeric(df["Day7_Return"], errors="coerce").dropna()
    return x.mean() * 100 if len(x) else None

def fmt(x, suffix=""):
    return "N/A" if x is None or pd.isna(x) else f"{x:,.2f}{suffix}"

nps = nps_score(happiness)
csat = pd.to_numeric(happiness["CSAT Response"], errors="coerce").mean() if "CSAT Response" in happiness else None
sus = sus_score(happiness)
ces = pd.to_numeric(happiness["CES Response"], errors="coerce").mean() if "CES Response" in happiness else None
ttfv = ttfv_score(customers)
error_rate = task_error(task_success)
completion = task_completion(task_success)
adoption_rate = core_action(adoption)
retention_rate = day7(retention)

st.sidebar.title("☕ Café Analytics")
page = st.sidebar.radio("Dashboard", [
    "Executive Overview", "Happiness", "Engagement", "Adoption",
    "Retention", "Task Success", "Orders & Customers"
])
st.sidebar.markdown("---")
st.sidebar.caption("Data source: Cafe_Analysis_Performed.xlsx")
st.sidebar.caption("Synthetic dataset for educational purposes.")

if page == "Executive Overview":
    st.title("☕ Café Behavioral Analytics Dashboard")
    st.write("Customer experience, engagement, adoption, retention, task success and ordering behavior.")

    st.subheader("Key Performance Indicators")
    c = st.columns(5)
    c[0].metric("NPS", fmt(nps))
    c[1].metric("CSAT", fmt(csat, " / 5"))
    c[2].metric("SUS", fmt(sus, " / 100"))
    c[3].metric("CES", fmt(ces, " / 7"))
    c[4].metric("TTFV", fmt(ttfv, " min"))

    c = st.columns(4)
    c[0].metric("Task Error Rate", fmt(error_rate, "%"))
    c[1].metric("Task Completion", fmt(completion, "%"))
    c[2].metric("Core Action Rate", fmt(adoption_rate, "%"))
    c[3].metric("Day-7 Retention", fmt(retention_rate, "%"))

    st.subheader("HEART Framework")
    heart = pd.DataFrame({
        "Dimension": ["Happiness", "Engagement", "Adoption", "Retention", "Task Success"],
        "Metric": [
            f"NPS: {fmt(nps)}",
            f"Sessions: {engagement['Session ID'].nunique():,}" if "Session ID" in engagement else "N/A",
            f"Core Action: {fmt(adoption_rate, '%')}",
            f"Day-7 Return: {fmt(retention_rate, '%')}",
            f"Completion: {fmt(completion, '%')}"
        ]
    })
    st.dataframe(heart, use_container_width=True, hide_index=True)

    st.subheader("Order Summary")
    c = st.columns(4)
    revenue = pd.to_numeric(orders["Item Total"], errors="coerce").sum() if "Item Total" in orders else None
    units = pd.to_numeric(orders["Quantity"], errors="coerce").sum() if "Quantity" in orders else None
    order_count = orders["Order ID"].nunique() if "Order ID" in orders else None
    avg_order = orders["Order Total"].drop_duplicates().mean() if "Order Total" in orders else None
    c[0].metric("Revenue", fmt(revenue))
    c[1].metric("Units Sold", fmt(units))
    c[2].metric("Orders", fmt(order_count))
    c[3].metric("Average Order", fmt(avg_order))

elif page == "Happiness":
    st.title("😊 Happiness")
    c = st.columns(4)
    c[0].metric("NPS", fmt(nps))
    c[1].metric("CSAT", fmt(csat, " / 5"))
    c[2].metric("SUS", fmt(sus, " / 100"))
    c[3].metric("CES", fmt(ces, " / 7"))

    if "NPS Response" in happiness:
        fig = px.histogram(happiness, x="NPS Response", nbins=10, title="NPS Response Distribution")
        st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns(2)
    with a:
        if "CSAT Response" in happiness:
            x = happiness["CSAT Response"].value_counts().sort_index().reset_index()
            x.columns = ["CSAT Response", "Responses"]
            st.plotly_chart(px.bar(x, x="CSAT Response", y="Responses", title="CSAT Distribution"), use_container_width=True)
    with b:
        if "CES Response" in happiness:
            x = happiness["CES Response"].value_counts().sort_index().reset_index()
            x.columns = ["CES Response", "Responses"]
            st.plotly_chart(px.bar(x, x="CES Response", y="Responses", title="CES Distribution"), use_container_width=True)

    if "SUS Score" in happiness:
        st.plotly_chart(px.histogram(happiness, x="SUS Score", nbins=10, title="SUS Score Distribution"), use_container_width=True)

    if "NPS Comment" in happiness:
        st.subheader("NPS Comments")
        st.dataframe(happiness[["NPS Response", "NPS Comment"]].dropna(subset=["NPS Comment"]),
                     use_container_width=True, hide_index=True)

elif page == "Engagement":
    st.title("📈 Engagement")
    sessions = engagement["Session ID"].nunique() if "Session ID" in engagement else 0
    events = len(engagement)
    seconds = pd.to_numeric(engagement["Engagement Seconds"], errors="coerce").sum() if "Engagement Seconds" in engagement else 0
    meaningful = engagement["Meaningful Value"].notna().sum() if "Meaningful Value" in engagement else 0

    c = st.columns(4)
    c[0].metric("Unique Sessions", f"{sessions:,}")
    c[1].metric("Total Events", f"{events:,}")
    c[2].metric("Engagement Time", f"{seconds / 60:,.1f} min")
    c[3].metric("Meaningful Value Events", f"{meaningful:,}")

    if "Event Type" in engagement:
        x = engagement["Event Type"].value_counts().reset_index()
        x.columns = ["Event Type", "Count"]
        st.plotly_chart(px.bar(x, x="Event Type", y="Count", title="Events by Type"), use_container_width=True)

    if "Page" in engagement:
        x = engagement["Page"].value_counts().head(15).reset_index()
        x.columns = ["Page", "Visits"]
        st.plotly_chart(px.bar(x, x="Visits", y="Page", orientation="h", title="Most Visited Pages"), use_container_width=True)

elif page == "Adoption":
    st.title("🚀 Adoption")

    c = st.columns(2)
    c[0].metric("Core Action Rate", fmt(adoption_rate, "%"))
    c[1].metric(
        "Adoption Sessions",
        f"{adoption['Session ID'].nunique():,}"
        if "Session ID" in adoption else "N/A"
    )

    if "Action" in adoption:
        x = adoption["Action"].value_counts().reset_index()
        x.columns = ["Action", "Count"]

        st.plotly_chart(
            px.bar(
                x,
                x="Action",
                y="Count",
                title="Actions Performed"
            ),
            use_container_width=True
        )

    # User Adoption Funnel
    if {"User ID", "Action"}.issubset(adoption.columns):

        login_users = adoption.loc[
            adoption["Action"] == "User Login", "User ID"
        ].nunique()

        cart_users = adoption.loc[
            adoption["Action"] == "Add to Cart", "User ID"
        ].nunique()

        order_users = adoption.loc[
            adoption["Action"] == "Order Completed", "User ID"
        ].nunique()

        funnel_data = pd.DataFrame({
            "Stage": [
                "Logged In",
                "Added Product to Cart",
                "Ordered Product"
            ],
            "Users": [
                login_users,
                cart_users,
                order_users
            ]
        })

        st.subheader("User Adoption Funnel")

        st.plotly_chart(
            px.funnel(
                funnel_data,
                y="Stage",
                x="Users",
                title="Login → Cart → Order"
            ),
            use_container_width=True
        )

        f1, f2, f3 = st.columns(3)
        f1.metric("Logged In", f"{login_users:,}")
        f2.metric("Added to Cart", f"{cart_users:,}")
        f3.metric("Ordered", f"{order_users:,}")
elif page == "Retention":
    st.title("🔄 Retention")
    c = st.columns(3)
    c[0].metric("Day-7 Return Rate", fmt(retention_rate, "%"))
    c[1].metric("Users", f"{retention['User ID'].nunique():,}" if "User ID" in retention else f"{len(retention):,}")
    c[2].metric("Maximum Visit Number",
                f"{pd.to_numeric(retention['Visit Number'], errors='coerce').max():,.0f}" if "Visit Number" in retention else "N/A")

    if "Day7_Return" in retention:
        x = pd.to_numeric(retention["Day7_Return"], errors="coerce").value_counts().sort_index().reset_index()
        x.columns = ["Day7_Return", "Count"]
        st.plotly_chart(px.bar(x, x="Day7_Return", y="Count", title="Day-7 Return Distribution"), use_container_width=True)

    if "Visit Number" in retention:
        x = retention["Visit Number"].value_counts().sort_index().reset_index()
        x.columns = ["Visit Number", "Records"]
        st.plotly_chart(px.bar(x, x="Visit Number", y="Records", title="Visit Number Distribution"), use_container_width=True)

elif page == "Task Success":
    st.title("✅ Task Success")
    attempts = pd.to_numeric(task_success["Task Attempt Flag"], errors="coerce").sum() if "Task Attempt Flag" in task_success else None
    errors = pd.to_numeric(task_success["Error Count"], errors="coerce").sum() if "Error Count" in task_success else None

    c = st.columns(4)
    c[0].metric("Task Completion", fmt(completion, "%"))
    c[1].metric("Task Error Rate", fmt(error_rate, "%"))
    c[2].metric("Task Attempts", fmt(attempts))
    c[3].metric("Total Errors", fmt(errors))

    if "Status" in task_success:
        x = task_success["Status"].value_counts().reset_index()
        x.columns = ["Status", "Count"]
        st.plotly_chart(px.pie(x, names="Status", values="Count", title="Task Status"), use_container_width=True)

    if "Task" in task_success:
        x = task_success["Task"].value_counts().reset_index()
        x.columns = ["Task", "Records"]
        st.plotly_chart(px.bar(x, x="Task", y="Records", title="Task Activity"), use_container_width=True)

elif page == "Orders & Customers":
    st.title("🛒 Orders & Customer Behaviour")
    revenue = pd.to_numeric(orders["Item Total"], errors="coerce").sum() if "Item Total" in orders else 0
    units = pd.to_numeric(orders["Quantity"], errors="coerce").sum() if "Quantity" in orders else 0
    order_count = orders["Order ID"].nunique() if "Order ID" in orders else 0
    avg_order = orders["Order Total"].drop_duplicates().mean() if "Order Total" in orders else None

    c = st.columns(4)
    c[0].metric("Revenue", fmt(revenue))
    c[1].metric("Units Sold", f"{units:,.0f}")
    c[2].metric("Orders", f"{order_count:,}")
    c[3].metric("Average Order", fmt(avg_order))

    if "Product Name" in orders:
        product = orders.groupby("Product Name").agg(
            Units=("Quantity", "sum"), Revenue=("Item Total", "sum")
        ).reset_index().sort_values("Revenue", ascending=False)

        st.plotly_chart(
            px.bar(product.head(15), x="Revenue", y="Product Name", orientation="h",
                   title="Top Products by Revenue"),
            use_container_width=True
        )
        st.subheader("Product Performance")
        st.dataframe(product, use_container_width=True, hide_index=True)

    if not customers.empty:
        st.subheader("Customer Overview")
        c = st.columns(4)
        if "User ID" in customers:
            c[0].metric("Customers", f"{customers['User ID'].nunique():,}")
        if "Total Sessions" in customers:
            c[1].metric("Avg Sessions / Customer",
                        fmt(pd.to_numeric(customers["Total Sessions"], errors="coerce").mean()))
        if "Orders Count" in customers:
            c[2].metric("Avg Orders / Customer",
                        fmt(pd.to_numeric(customers["Orders Count"], errors="coerce").mean()))
        if "Returning User" in customers:
            returning = customers["Returning User"].astype(str).str.lower().eq("yes").mean() * 100
            c[3].metric("Returning Customers", f"{returning:.2f}%")
