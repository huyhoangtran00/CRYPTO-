#include <gmpxx.h>
#include <iostream>
#include <fstream>
#include <random>

struct Point {
    mpz_class x;
    mpz_class y;
    bool at_infinity;

    Point() : at_infinity(true) {}
    Point(mpz_class x, mpz_class y) : x(x), y(y), at_infinity(false) {}
};

// Hàm kiểm tra điểm có nằm trên đường cong không
bool is_on_curve(const Point& P, const mpz_class& A, const mpz_class& B, const mpz_class& p) {
    if (P.at_infinity) return true;
    mpz_class left = (P.y * P.y) % p;
    mpz_class right = (P.x * P.x * P.x + A * P.x + B) % p;
    return left == right;
}

// Hàm cộng hai điểm trên đường cong elliptic
Point point_addition(const Point& P, const Point& Q, const mpz_class& A, const mpz_class& p) {
    if (P.at_infinity) return Q;
    if (Q.at_infinity) return P;

    mpz_class slope;
    if (P.x == Q.x && P.y == Q.y) {
        mpz_class num = 3 * P.x * P.x + A;
        mpz_class denom = 2 * P.y;
        if (mpz_invert(denom.get_mpz_t(), denom.get_mpz_t(), p.get_mpz_t()) == 0)
            return Point();  // Trả về điểm ở vô cực nếu phép nghịch đảo không hợp lệ
        slope = (num * denom) % p;
    } else {
        mpz_class num = Q.y - P.y;
        mpz_class denom = Q.x - P.x;
        if (mpz_invert(denom.get_mpz_t(), denom.get_mpz_t(), p.get_mpz_t()) == 0)
            return Point();  // Trả về điểm ở vô cực nếu phép nghịch đảo không hợp lệ
        slope = (num * denom) % p;
    }

    mpz_class xr = (slope * slope - P.x - Q.x) % p;
    if (xr < 0) xr += p;
    mpz_class yr = (slope * (P.x - xr) - P.y) % p;
    if (yr < 0) yr += p;

    return Point(xr, yr);
}

// Hàm nhân vô hướng trên đường cong elliptic
Point point_multiplication(const mpz_class& k, const Point& G, const mpz_class& A, const mpz_class& p) {
    Point result;
    Point addend = G;
    mpz_class temp_k = k;

    while (temp_k > 0) {
        if (temp_k % 2 == 1) {
            result = point_addition(result, addend, A, p);
        }
        addend = point_addition(addend, addend, A, p);
        temp_k /= 2;
    }

    return result;
}



// Hàm sinh khóa ECDSA
std::pair<mpz_class, Point> generate_keys(const Point& G, const mpz_class& n, const mpz_class& A, const mpz_class& p) {
    mpz_class private_key;
    Point public_key;

    gmp_randclass rand_gen(gmp_randinit_default);
    rand_gen.seed(time(nullptr));

    private_key = rand_gen.get_z_range(n);
    public_key = point_multiplication(private_key, G, A, p);

    return {private_key, public_key};
}

// Hàm ký ECDSA
std::pair<mpz_class, mpz_class> ecdsa_sign(const mpz_class& message, const mpz_class& private_key, const Point& G, const mpz_class& n, const mpz_class& A, const mpz_class& p) {
    mpz_class r, s;
    gmp_randclass rand_gen(gmp_randinit_default);
    rand_gen.seed(time(nullptr));

    while (true) {
        mpz_class k = rand_gen.get_z_range(n);  // Chọn số ngẫu nhiên k
        Point kG = point_multiplication(k, G, A, p);

        r = kG.x % n;
        if (r == 0) continue;

        mpz_class k_inv;
        mpz_invert(k_inv.get_mpz_t(), k.get_mpz_t(), n.get_mpz_t());
        s = (k_inv * (message + private_key * r)) % n;
        
        if (s != 0) break;
    }

    return {r, s};
}

// Hàm xác minh ECDSA
bool ecdsa_verify(const mpz_class& message, const std::pair<mpz_class, mpz_class>& signature, const Point& public_key, const Point& G, const mpz_class& n, const mpz_class& A, const mpz_class& p) {
    mpz_class r = signature.first;
    mpz_class s = signature.second;

    if (r <= 0 || r >= n || s <= 0 || s >= n) return false;

    mpz_class s_inv;
    mpz_invert(s_inv.get_mpz_t(), s.get_mpz_t(), n.get_mpz_t());

    mpz_class u1 = (message * s_inv) % n;
    mpz_class u2 = (r * s_inv) % n;

    Point u1G = point_multiplication(u1, G, A, p);
    Point u2Q = point_multiplication(u2, public_key, A, p);
    Point point_sum = point_addition(u1G, u2Q, A, p);

    return (point_sum.x % n) == r;
}
bool is_non_singular(const mpz_class& A, const mpz_class& B, const mpz_class& p) {
    mpz_class term1 = 4 * A * A * A % p;
    mpz_class term2 = 27 * B * B % p;
    mpz_class result = (term1 + term2) % p;
    return result != 0;
}



int main() {
    mpz_class p("AADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA703308717D4D9B009BC66842AECDA12AE6A380E62881FF2F2D82C68528AA6056583A48F3", 16);
    mpz_class A("7830A3318B603B89E2327145AC234CC594CBDD8D3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CA", 16);
    mpz_class B("3DF91610A83441CAEA9863BC2DED5D5AA8253AA10A2EF1C98B9AC8B57F1117A72BF2C7B9E7C1AC4D77FC94CADC083E67984050B75EBAE5DD2809BD638016F723", 16);
    

    Point G(
        mpz_class("81AEE4BDD82ED9645A21322E9C4C6A9385ED9F70B5D916C1B43B62EEF4D0098EFF3B1F78E2D0D48D50D1687B93B97D5F7C6D5047406A5E688B352209BCB9F822", 16),
        mpz_class("7DDE385D566332ECC0EABFA9CF7822FDF209F70024A57B1AA000C55B881F8111B2DCDE494A5F485E5BCA4BD88A2763AED1CA2B2FA8F0540678CD1E0F3AD80892", 16)
    );




    mpz_class y_doi = p - G.y;
    std::ofstream outfile("points_from_generator.txt");
    if (!outfile.is_open()) {
        std::cerr << "Unable to open file for writing." << std::endl;
        return 1;
    }
    // Ghi các điểm sinh và các thông số khác vào file
    outfile << "Tham số đường cong\n";
    outfile << "a: " << A.get_str() << "\n";
    outfile << "b: " << B.get_str() << "\n";
    outfile << "p: " << p.get_str() << "\n";
    outfile << "Ta được đường cong" << std::endl;
    outfile << "y^2 = x^3 + " << A.get_str() << "x + " << B.get_str() << " (mod " << p.get_str() << ")\n";
        // Kiểm tra điều kiện không suy biến của đường cong
    
    if (!is_non_singular(A, B, p)) {
        std::cout << "Đường cong không thỏa mãn (4a^3 + 27b^2 ≡ 0 mod p)!!!" << std::endl;
        outfile << "Đường cong không thỏa mãn  (4a^3 + 27b^2 ≡ 0 mod p)!!!" << std::endl;
        return 1;
    }
    else {
        std::cout << "Đường cong eliptic thỏa mãn !!!" << std::endl;
        outfile << "Đường cong eliptic thỏa mãn !!!" << std::endl;
    }
        outfile << std::endl;
    outfile << std::endl;

    outfile << "Điểm sinh (G):\n";
    outfile << "x: " << G.x.get_str() << "\n";
    outfile << "y: " << G.y.get_str() << "\n";
    outfile << "Điểm đối của điểm sinh:\n";
    outfile << "x: " << G.x.get_str() << "\n";
    outfile << "y: " << y_doi.get_str() << "\n";





    // Kiểm tra xem điểm sinh có nằm trên đường cong không
    if (!is_on_curve(G, A, B, p)) {
        std::cerr << "Điểm sinh được xác thực không nằm trên đường cong !!!" << std::endl;
        outfile << "Điểm sinh được xác thực không nằm trên đường cong" << std::endl;
        return 1;
    }
    else {
        std::cout << "Điểm sinh được xác thực nằm trên đường cong !!!" << std::endl;
        outfile << "Điểm sinh được xác thực nằm trên đường cong !!!" << std::endl;
}

        outfile << std::endl;
    outfile << std::endl;
    // Thực hiện các thao tác tiếp theo (ví dụ: sinh khóa, ký và xác minh)

    // Tính tổng số điểm (bậc của điểm sinh G)

    mpz_class n("8948962207650232551656602815159153422162609644098354511344597187200057010413418528378981730643524959857451398370029280583094215613882043973354392115544169", 10);
    outfile << "Tổng số điểm trên đường cong: " << n.get_str() << std::endl;
    // Sinh khóa
    auto [private_key, public_key] = generate_keys(G, n, A, p);
    std::cout << "Private key: " << private_key.get_str() << "\n";
    std::cout << "Public key: (" << public_key.x.get_str() << ", " << public_key.y.get_str() << ")\n";
    outfile << "Private key: " << private_key.get_str() << std::endl;
    outfile << "Public key: (" << public_key.x.get_str() << ", " << public_key.y.get_str() << ")" << std::endl;
    // Message
    mpz_class message("20160091143476977738780");
    std::cout << "Message: " << message.get_str() << "\n";
    // Ký
    auto signature = ecdsa_sign(message, private_key, G, n, A, p);
    std::cout << "Signature (r, s): (" << signature.first.get_str() << ", " << signature.second.get_str() << ")\n";
    outfile << "Signature (r, s): (" << signature.first.get_str() << ", " << signature.second.get_str() << ")" << std::endl;
    // Xác minh
    bool is_valid = ecdsa_verify(message, signature, public_key, G, n, A, p);
    if (is_valid) {
        std::cout << "Chữ ký hợp lệ\n";
        outfile << "Chữ ký hợp lệ!!!" << std::endl;
    } else {
        std::cout << "Chữ ký không hợp lệ\n";
        outfile << "Chữ ký không hợp lệ!!!" << std::endl;
    }
    
    outfile.close();
    return 0;
}
