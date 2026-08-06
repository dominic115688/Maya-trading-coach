import streamlit as st
import sqlite3
from ai.coach import get_ai_coach_response
from database.db import init_db, register_user, verify_user, log_chat, get_chat_history, clear_chat_history, log_trade, get_trades

# Initialize Database
init_db()

st.set_page_config(page_title="Maya - AI Trading Coach", page_icon="📈", layout="centered")

# Initialize Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# ----------------- AUTHENTICATION SCREEN -----------------
if not st.session_state.authenticated:
    st.title("🔒 Maya AI Trading Coach - Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if verify_user(login_user, login_pass):
                st.session_state.authenticated = True
                st.session_state.username = login_user
                st.rerun()
            else:
                st.error("Invalid username or password.")
                
    with tab2:
        reg_user = st.text_input("Choose Username", key="reg_user")
        reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        if st.button("Register Account"):
            if register_user(reg_user, reg_pass):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists.")

# ----------------- MAIN DASHBOARD -----------------
else:
    username = st.session_state.username
    
    # Sidebar for Navigation & Controls
    st.sidebar.title(f"Welcome, {username}!")
    
    lang = st.sidebar.selectbox("Language / Idioma", ["English", "Spanish"])
    
    if st.sidebar.button("🗑️ Clear Chat History"):
        clear_chat_history(username)
        st.rerun()
        
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    st.title("🤖 Maya — AI Trading Coach")
    
    # Tabs for Chat, Trade Logging, and History
    tab_chat, tab_lookup, tab_log, tab_history = st.tabs(["💬 Chat with Maya", "🔍 Symbol Lookup", "📝 Log Trade", "📊 Trade History"])
    
    # --- TAB 1: CHAT INTERFACE ---
    with tab_chat:
        # Load chat history from DB
        history = get_chat_history(username)
        
        for sender, msg in history:
            role = "user" if sender == username else "assistant"
            with st.chat_message(role):
                st.markdown(f"**{sender}**: {msg}")
                
        # Chat input box
        prompt = st.chat_input("Ask Maya a trading question...")
        if prompt:
            # Display user message
            with st.chat_message("user"):
                st.markdown(f"**{username}**: {prompt}")
            log_chat(username, username, prompt)
            
            # Get AI Response
            with st.chat_message("assistant"):
                with st.spinner("Maya is analyzing..."):
                    ai_response = get_ai_coach_response(prompt, language=("Spanish" if lang == "Spanish" else "English"))
                st.markdown(f"**Maya**: {ai_response}")
            log_chat(username, "Maya", ai_response)
            st.rerun()

    # --- TAB 2: SYMBOL LOOKUP & RISK VERIFICATION ---
    with tab_lookup:
        st.subheader("Verify Hot Tips & Growth Claims")
        lookup_symbol = st.text_input("Ticker Symbol or Company Name (e.g. AAPL, TSLA)")
        lookup_claim = st.text_area("What did someone claim about it?", placeholder="e.g., They are growing 300% a year and expanding fast...")
        
        if st.button("Analyze Tip with Maya"):
            if lookup_symbol:
                analysis_prompt = f"Analyze the company/symbol '{lookup_symbol}'. Someone claimed: '{lookup_claim if lookup_claim else 'It is growing fast and is a great investment'}'. Evaluate potential risks, sudden collapse hazards versus steady growth, valuation sanity, and provide a coaching verdict."
                
                with st.spinner("Maya is evaluating market reality..."):
                    verdict = get_ai_coach_response(analysis_prompt, language=("Spanish" if lang == "Spanish" else "English"))
                
                st.success("Analysis Complete!")
                st.markdown(verdict)
                log_chat(username, username, f"Verify Symbol: {lookup_symbol}")
                log_chat(username, "Maya", verdict)
            else:
                st.warning("Please enter a symbol or company name.")

    # --- TAB 3: LOG TRADE ---
    with tab_log:
        st.subheader("Record a New Trade Setup")
        with st.form("trade_form"):
            t_symbol = st.text_input("Symbol (e.g. BTC, MSFT)").upper()
            t_price = st.number_input("Entry Price", min_value=0.0, format="%.2f")
            t_size = st.number_input("Position Size (Shares/Units)", min_value=0.0, format="%.4f")
            t_type = st.selectbox("Trade Type", ["Long", "Short"])
            t_notes = st.text_area("Strategy Rationale / Notes")
            
            submitted = st.form_submit_button("Save Trade to Database")
            if submitted:
                if t_symbol:
                    log_trade(username, t_symbol, t_price, t_size, t_type, t_notes)
                    st.success(f"Trade for {t_symbol} successfully logged!")
                else:
                    st.error("Please enter a valid symbol.")

    # --- TAB 4: TRADE HISTORY ---
    with tab_history:
        st.subheader("Your Saved Trades")
        trades = get_trades(username)
        if trades:
            st.dataframe(trades, use_container_width=True)
        else:
            st.info("No saved trades found yet. Use the 'Log Trade' tab to add your setups.")