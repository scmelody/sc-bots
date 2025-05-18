from logic.code_redeemer import redeem_all_codes
from utils.state import BotContext

def main():
    print("🚀 Ragnarok Redeem Bot เริ่มทำงาน")
    ctx = BotContext(config_path="config.json")
    redeem_all_codes(ctx)

if __name__ == "__main__":
    main()
