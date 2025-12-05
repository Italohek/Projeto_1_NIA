import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { DollarSign, ShoppingCart, Users } from "lucide-react";

const FiltersSection = () => {
  const [stats, setStats] = useState({
    total_revenue: 0,
    total_sales: 0,
    total_customers: 0,
  });
  const [activity, setActivity] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [limit, setLimit] = useState(10);
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null);

  // abaixo temos as funcões para buscar as informacões e ambas são separadas tendo em vista que a requisicão duplicada
  // iria diminuir a performance, portanto isso se torna necessário

  // função para dar um fetch nos stats
  const fetchStats = async (month: number | null) => {
    try {
      const url = month
        ? `http://127.0.0.1:8000/getStats/stats?month=${month}`
        : "http://127.0.0.1:8000/getStats/stats";

      const res = await fetch(url);
      if (!res.ok) throw new Error("Erro ao buscar /stats");
      const data = await res.json();
      setStats(data);
    } catch (error) {
      console.error("❌ Erro ao buscar estatísticas:", error);
    }
  };

  // função para buscar as atividades 
  const fetchActivity = async (limit: number) => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/overviewSection/recent-activity?limit=${limit}`
      );
      if (!res.ok) throw new Error("Erro ao buscar /recent-activity");
      const data = await res.json();
      setActivity(data);
    } catch (error) {
      console.error("❌ Erro ao buscar atividades:", error);
    }
  };

  // busca as estatísticas quando o mês mudar
  useEffect(() => {
    setLoading(true);
    Promise.all([fetchStats(selectedMonth), fetchActivity(limit)]).finally(() =>
      setLoading(false)
    );
  }, [selectedMonth]);

  // busca a atividade recente ao apertar enter
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      fetchActivity(limit);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(event.target.value);
    setLimit(Number.isNaN(value) ? 0 : value);
  };

  const handleMonthChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const month = event.target.value ? parseInt(event.target.value) : null;
    setSelectedMonth(month);
  };

  const statCards = [
    {
      title: "Receita Total",
      value: `R$ ${stats.total_revenue.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
      })}`,
      icon: DollarSign,
      color: "text-green-500",
    },
    {
      title: "Vendas",
      value: stats.total_sales.toLocaleString("pt-BR"),
      icon: ShoppingCart,
      color: "text-blue-500",
    },
    {
      title: "Clientes",
      value: stats.total_customers.toLocaleString("pt-BR"),
      icon: Users,
      color: "text-purple-500",
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-40">
        <p className="text-muted-foreground">Carregando dados...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* seletor de mês */}
      <div className="flex items-center gap-4">
        <label htmlFor="month-select" className="text-sm font-medium">
          Selecione o mês:
        </label>
        <select
          id="month-select"
          className="border rounded px-2 py-1"
          onChange={handleMonthChange}
          value={selectedMonth ?? ""}
        >
          <option value="">Todos os meses</option>
          {Array.from({ length: 7 }, (_, i) => i + 5).map((month) => (
            <option key={month} value={month}>
              {new Date(2023, month - 1).toLocaleString("pt-BR", {
                month: "long",
              })}
            </option>
          ))}
        </select>
      </div>

      {/* janela de status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {statCards.map((stat, index) => (
          <Card
            key={index}
            className="glass-card p-6 hover:shadow-xl transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">
                  {stat.title}
                </p>
                <h3 className="text-2xl font-bold mb-2">{stat.value}</h3>
              </div>
              <div
                className={`w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center ${stat.color}`}
              >
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* atividade recente */}
      <Card className="glass-card p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Atividade Recente</h3>
          <div className="flex items-center gap-2">
            <label htmlFor="limit" className="font-medium">
              Itens:
            </label>
            <input
              id="limit"
              type="number"
              min={1}
              value={limit}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              className="border rounded px-2 py-1 w-20"
            />
          </div>
        </div>

        <div className="space-y-3 max-h-80 overflow-y-auto pr-2">
          {activity.length > 0 ? (
            activity.map((act, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div
                  className={`w-2 h-2 rounded-full ${
                    act.type === "success" ? "bg-green-500" : "bg-blue-500"
                  }`}
                />
                <span className="text-sm text-muted-foreground">
                  {act.time}
                </span>
                <span className="text-sm flex-1">{act.desc}</span>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted-foreground">
              Nenhuma atividade recente encontrada.
            </p>
          )}
        </div>
      </Card>
    </div>
  );
};

export default FiltersSection;