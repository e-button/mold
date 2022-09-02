def haha():
    import csv
    from app.models import Staff, MoldData, Machine, Process
    file = open('/Users/admin/cloud/coding/yw_app/data.csv')

    csvreader = csv.reader(file)
    for row in csvreader:
        staff_name = row[0]
        staff = Staff.objects.get(name=staff_name)
        machine_no = row[1]
        machine = Machine.objects.get(no=machine_no)
        process_type = row[2]
        process = Process.objects.get(type=process_type)
        mod_no = row[3]
        start_time = row[4]
        status = 1
        # end_time = '0000-00-00 00:00:00'
        m = MoldData(
            start_time=start_time,
            # end_time=end_time,
            status=status,
            staff=staff,
            machine=machine,
            process=process,
            mod_no=mod_no
        )
        m.save()
