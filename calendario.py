import calendar

# Configurar para começar na segunda-feira
calendar.setfirstweekday(calendar.MONDAY)

ano_2025 = 2025

print(f"CALENDÁRIO 2025 (começando na segunda-feira)")
print("=" * 40)

# Criar calendário personalizado
cal = calendar.TextCalendar(calendar.MONDAY)

# Mostrar todos os meses
for mes in range(1, 13):
    print(f"\n{calendar.month_name[mes].upper()} {ano_2025}")
    print(cal.formatmonth(ano_2025, mes))