# main.py - entry point
import os,sys,traceback
def main():
    try:from app import App
    except ImportError as e:print(f"error import: {e}");traceback.print_exc();sys.exit(1)
    x=App();x.mainloop()
if __name__=="__main__":main()
