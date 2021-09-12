from webbrowser import get
from servicefile import Create_Service
import pandas as pd
import streamlit as st
import time
import base64
import io, os
import itertools

CLIENT_SECRET_FILE = 'D:\Projects\Extract Google Drive Links\client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Update Sharing Setting
st.title('Extract Google Drive Links')
file_id = st.text_input('')
fileids=list(file_id.split(','))
# print(fileids)

request_body = {
    'role': 'reader',
    'type': 'anyone'
}

for i in fileids:
    response_permission = service.permissions().create(
        fileId=i,
        body=request_body
    ).execute()

# # print(response_permission)


# # Print Sharing URL
# response_share_link = service.files().get(
#     fileId=file_id,
#     fields='webViewLink'
# ).execute()

# print(response_share_link)

# Remove Sharing Permission
# service.permissions().delete(
#     fileId=file_id,
#     permissionId='anyoneWithLink'
# ).execute()
list_of_files=[]
if file_id=='':
    'Pls enter folder or file id'
else:
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        latest_iteration.text(f'Progress {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    for j in fileids:
        query=f"parents='{j}'"
        response=service.files().list(q=query).execute()
        files=response.get('files')
        idvalues=[d.get('id') for d in files]
        list_of_files.extend(idvalues)
        # nextpageToken=response.get('nextPageToken')
        # while nextpageToken:
        #     response=service.files().list(q=query).execute()
        #     files.extend()
        #     nextpageToken=response.get('nextPageToken')


    df=pd.DataFrame(list_of_files,columns=['fileid'])
    towrite = io.BytesIO()
    df['file link']='https://drive.google.com/file/d/'+df['fileid']
    st.write('Extraction is Completed')
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="GoogleDriveLinks.xlsx">Download file</a>'
    st.markdown(linko, unsafe_allow_html=True)

