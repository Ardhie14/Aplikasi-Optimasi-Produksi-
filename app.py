def main():
    st.set_page_config(page_title="Optimasi Produksi - Linear Programming", layout="centered")
    st.title("📈 Aplikasi Optimasi Produksi (Linear Programming)")
    st.sidebar.header("📋 Instruksi:")
    st.sidebar.markdown("""
    1. Masukkan jumlah produk & keuntungan/unit  
    2. Masukkan batasan sumber daya  
    3. Klik tombol 'Hitung Solusi Optimal'  
    4. Lihat hasil dan visualisasi  
    """)

    st.subheader("1️⃣ Masukkan Data Produksi")
    n = st.number_input("Jumlah Produk", min_value=2, max_value=5, value=2)

    produk = []
    profit = []
    for i in range(n):
        produk.append(st.text_input(f"Nama Produk {i+1}", value=f"P{i+1}"))
        profit.append(st.number_input(f"Keuntungan per unit {produk[i]}", value=0.0))

    st.subheader("2️⃣ Masukkan Batasan Sumber Daya")
    m = st.number_input("Jumlah Batasan (Kendala)", min_value=1, max_value=5, value=2)
    batasan = []
    batas = []

    for j in range(m):
        st.markdown(f"**Kendala {j+1}**")
        row = []
        for i in range(n):
            row.append(st.number_input(f"Koefisien {produk[i]} (Kendala {j+1})", value=0.0, key=f"x{i}_c{j}"))
        batasan.append(row)
        batas.append(st.number_input(f"Nilai Maksimum Kendala {j+1}", value=0.0, key=f"rhs_{j}"))

    if st.button("📊 Hitung Solusi Optimal"):
        hasil = linprog(
            c=[-p for p in profit],       # Maksimasi = minimisasi -Z
            A_ub=batasan,
            b_ub=batas,
            method='highs'
        )

        if hasil.success:
            st.success("✅ Solusi ditemukan!")
            total_profit = -hasil.fun
            for i in range(n):
                st.write(f"Produksi {produk[i]} = {hasil.x[i]:.2f}")
            st.write(f"💰 **Total Keuntungan: {total_profit:.2f}**")

            if n == 2:
                show_visualization(batasan, batas, hasil.x, produk)

        else:
            st.error("❌ Tidak ditemukan solusi optimal.")

def show_visualization(A, b, sol, produk):
    x = np.linspace(0, 50, 400)
    plt.figure(figsize=(7,5))
    for i in range(len(A)):
        if A[i][1] != 0:
            y = (b[i] - A[i][0]*x)/A[i][1]
            plt.plot(x, y, label=f'Kendala {i+1}')
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.scatter(sol[0], sol[1], color='red', zorder=5, label='Solusi Optimal')
    plt.xlabel(produk[0])
    plt.ylabel(produk[1])
    plt.xlim(0, max(sol[0]*1.5, 10))
    plt.ylim(0, max(sol[1]*1.5, 10))
    plt.legend()
    plt.title("Area Feasible & Solusi Optimal")
    st.pyplot(plt)

if __name__ == "__main__":
    main()
