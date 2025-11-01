import streamlit as st
import pandas as pd

# ============================
# Load your merged data
# ============================
df = pd.read_excel("crop_data.xlsx")
# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Optional: check what columns exist
print(df.columns)


st.title("🌾 Project Samarth - Intelligent Data Q&A System")
st.write("Ask natural language questions about crop production and rainfall data across Indian states.")

question = st.text_input("Enter your question:")

# When button is pressed
if st.button("Get Answer"):

    q = question.lower()

    # ✅ Question Type 1: Compare rainfall between two states
    if "compare" in q and "rainfall" in q:
        import re
        match = re.findall(r"in ([a-z &]+) and ([a-z &]+)", q)
        if match:
            state1, state2 = match[0]
            s1 = df[df["STATE"].str.lower().str.contains(state1.strip())]
            s2 = df[df["STATE"].str.lower().str.contains(state2.strip())]

            if not s1.empty and not s2.empty:
                avg1 = s1["AVERAGE RAINFALL"].mean()
                avg2 = s2["AVERAGE RAINFALL"].mean()

                st.subheader("📊 Rainfall Comparison")
                st.write(f"**{state1.title()}** → Average Rainfall: {avg1:.2f} mm")
                st.write(f"**{state2.title()}** → Average Rainfall: {avg2:.2f} mm")

                if avg1 > avg2:
                    st.success(f"{state1.title()} receives {avg1 - avg2:.2f} mm more rainfall than {state2.title()}.")
                else:
                    st.info(f"{state2.title()} receives {avg2 - avg1:.2f} mm more rainfall than {state1.title()}.")
            else:
                st.warning("Couldn't find one or both states in the dataset.")
        else:
            st.warning("Try asking: Compare rainfall in Karnataka and Kerala.")

    # ✅ Question Type 2: Production trend of a state
    elif "trend" in q and "production" in q:
        import re
        match = re.findall(r"in ([a-z &]+)", q)
        if match:
            state = match[0]
            s = df[df["STATE"].str.lower().str.contains(state.strip())]
            if not s.empty:
                trend = s.groupby("YEAR")["PRODUCTION_1"].sum().reset_index()
                st.subheader(f"📈 Production Trend in {state.title()}")
                st.line_chart(trend.set_index("YEAR"))
            else:
                st.warning("No data found for that state.")
        else:
            st.warning("Try asking: Show production trend in Tamil Nadu.")

    # ✅ Question Type 3: Correlation between rainfall and production
    elif "correlation" in q or ("relationship" in q and "rainfall" in q):
        import re
        match = re.findall(r"in ([a-z &]+)", q)
        if match:
            state = match[0]
            s = df[df["STATE"].str.lower().str.contains(state.strip())]
            if not s.empty:
                corr = s["PRODUCTION_1"].corr(s["AVERAGE RAINFALL"])
                st.subheader(f"🌦️ Correlation between Rainfall and Production in {state.title()}")
                st.write(f"Correlation coefficient: **{corr:.3f}**")
                if corr > 0.5:
                    st.success("High positive correlation — rainfall increases production.")
                elif corr < -0.5:
                    st.error("High negative correlation — rainfall reduces production.")
                else:
                    st.info("Weak or no correlation found.")
            else:
                st.warning("No data found for that state.")
        else:
            st.warning("Try asking: Show correlation between rainfall and production in Kerala.")

    else:
        st.warning("Sorry, I didn't understand that question format yet. Try asking about rainfall, production trend, or correlation.")