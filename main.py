#whatstk is a open source library which converts a whatsapp txt file into a dataframe
from whatstk import df_from_txt_whatsapp
import templates as templateUtils
import ai as openaiUtils
from dotenv import load_dotenv
from pytz import timezone 
from datetime import datetime, timedelta
import re
import ast

#convert the chat to df
df = df_from_txt_whatsapp("files/_chat.txt")


#drop the first two rows so beacuse the details are unnecessary 
clean_df = df.loc[2:,:]
print(clean_df)





pattern = r"{([^}]*)}"


load_dotenv('.env')





def whatsapp_summary():
    

        params   = openaiUtils.set_open_params()
        response = openaiUtils.gpt_turbo(templateUtils.chat_summary.format(clean_df['message']))
        res = response.choices[0].message.content.replace("\n", "").replace("  ", "").replace("'", "")
        print(res)
                
               
            

whatsapp_summary()
