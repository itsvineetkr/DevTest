from django.shortcuts import render
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from home.utils import send_mail


def index(request):
    return render(request, 'home/index.html')

def result(request):
    if request.method == "POST":
        if 'upload_file' in request.POST:
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            
            processed_df = df.groupby(['Cust State', 'Cust Pin']).agg({'DPD': 'sum'}).reset_index()
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file_path = f'media/data/processed_data_{current_time}.xlsx'
            processed_df.to_excel(output_file_path, index=False)

            processed_df.rename(columns={'Cust State': 'Cust_State', 'Cust Pin': 'Cust_Pin'}, inplace=True)
            data = processed_df.to_dict(orient="records")
            
            email = "tech@themedius.ai"
            send_mail(email, data)
            
            return render(request, 'home/result.html', {'data': data, 'output_file_path': output_file_path})
        
        elif 'download' in request.POST:
            output_file_path = request.POST['output_file_path']
            with open(output_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={output_file_path.split("/")[-1]}'
                return response
    return render(request, 'home/result.html')
