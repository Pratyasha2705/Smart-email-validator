import csv
from validator import validate_format, get_domain, check_mx, is_disposable

def validate_bulk(input_file, output_file):
    results = []

    total = 0
    valid = 0
    invalid = 0
    disposable = 0

    # ✅ Read file safely
    with open(input_file, 'r') as file:
        lines = file.read().splitlines()

    for line in lines[1:]:   # skip header
        email = line.strip()

        if not email:
            continue

        total += 1

        if not validate_format(email):
            status = "Invalid Format"
            invalid += 1
        else:
            domain = get_domain(email)

            if is_disposable(domain):
                status = "Disposable Email"
                disposable += 1
            elif not check_mx(domain):
                status = "No MX Record"
                invalid += 1
            else:
                status = "Valid"
                valid += 1

        results.append({"email": email, "status": status})

    # ✅ Save results to CSV
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["email", "status"])
        writer.writeheader()
        writer.writerows(results)

    print("✅ Bulk validation completed!")

    print("\n📊 Summary:")
    print("Total Emails:", total)
    print("Valid Emails:", valid)
    print("Invalid Emails:", invalid)
    print("Disposable Emails:", disposable)

    # 🔥 IMPORTANT: Return stats for GUI + graph
    return total, valid, invalid, disposable


# ✅ Allow direct run
if __name__ == "__main__":
    validate_bulk("emails.csv", "results.csv")