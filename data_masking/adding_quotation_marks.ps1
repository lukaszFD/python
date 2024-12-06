Import-Csv "C:\...\data_masking\platform.csv" | Export-Csv "output.csv" -NoTypeInformation -Force
(Get-Content "output.csv") | ForEach-Object { if ($_.StartsWith('"')) { $_ } else { $_ -replace '([^,]+)', '"$1"' } } | 
Set-Content "C:\...\data_masking\platform_out.csv"

