import { useEffect, useState } from "react";
import axios from "axios";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const weekdays = [
  { id: 0, name: "Domingo", short: "Dom" },
  { id: 1, name: "Segunda", short: "Seg" },
  { id: 2, name: "Terça", short: "Ter" },
  { id: 3, name: "Quarta", short: "Qua" },
  { id: 4, name: "Quinta", short: "Qui" },
  { id: 5, name: "Sexta", short: "Sex" },
  { id: 6, name: "Sábado", short: "Sáb" },
];

const WeekdayAnalysis = () => {
  const [selectedDay, setSelectedDay] = useState(1); // Monday by default
  const [weekdayData, setWeekdayData] = useState<Record<number, { hour: string; sales: number }[]>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const res = await axios.get("http://127.0.0.1:8000/weekdayAnalysis/weekdayAnalysis");
        setWeekdayData(res.data);
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <p className="text-center text-muted-foreground">Carregando dados...</p>;
  }

  const currentData = weekdayData[selectedDay] || [];
  const peakHour = currentData.reduce((prev, curr) =>
    curr.sales > prev.sales ? curr : prev, { hour: "--", sales: 0 });

  return (
    <div className="space-y-6">
      {/* Seleção de dia */}
      <Card className="glass-card p-6">
        <h3 className="text-xl font-bold mb-4">Selecione o Dia da Semana</h3>
        <div className="grid grid-cols-7 gap-2">
          {weekdays.map((day) => (
            <Button
              key={day.id}
              variant={selectedDay === day.id ? "default" : "outline"}
              className={selectedDay === day.id ? "gradient-primary" : ""}
              onClick={() => setSelectedDay(day.id)}
            >
              <span className="hidden sm:inline">{day.name}</span>
              <span className="sm:hidden">{day.short}</span>
            </Button>
          ))}
        </div>
      </Card>

      {/* Estatísticas */}
      {currentData.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="glass-card p-6">
              <p className="text-sm text-muted-foreground mb-1">Total de Vendas</p>
              <h3 className="text-3xl font-bold">
                {currentData.reduce((sum, item) => sum + item.sales, 0)}
              </h3>
            </Card>

            <Card className="glass-card p-6">
              <p className="text-sm text-muted-foreground mb-1">Horário de Pico</p>
              <h3 className="text-3xl font-bold">{peakHour.hour}</h3>
              <p className="text-sm text-blue-500 mt-2">{peakHour.sales} vendas</p>
            </Card>

            <Card className="glass-card p-6">
              <p className="text-sm text-muted-foreground mb-1">Média por Hora</p>
              <h3 className="text-3xl font-bold">
                {Math.round(currentData.reduce((sum, item) => sum + item.sales, 0) / currentData.length)}
              </h3>
              <p className="text-sm text-purple-500 mt-2">vendas/hora</p>
            </Card>
          </div>

          {/* Gráfico */}
          <Card className="glass-card p-6">
            <h3 className="text-xl font-bold mb-6">
              Vendas por Horário - {weekdays[selectedDay].name}
            </h3>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={currentData}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                  <XAxis dataKey="hour" tick={{ fill: "hsl(var(--muted-foreground))" }} />
                  <YAxis tick={{ fill: "hsl(var(--muted-foreground))" }} />
                  <Tooltip />
                  <Bar dataKey="sales" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </>
      ) : (
        <p className="text-center text-muted-foreground">Nenhum dado encontrado para este dia.</p>
      )}
    </div>
  );
};

export default WeekdayAnalysis;