import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, BarChart3, Filter, Calendar } from "lucide-react";
import OverviewSection from "@/components/dashboard/OverviewSection";
import WeekdayAnalysis from "@/components/dashboard/WeekdayAnalysis";
import FiltersSection from "@/components/dashboard/FiltersSection";

const Index = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    { id: 0, title: "Visão Geral", icon: BarChart3, component: OverviewSection },
    { id: 1, title: "Filtros Avançados", icon: Filter, component: FiltersSection },
    // filtros mais avançados para a análise mais específica dos dados.
    { id: 2, title: "Análise por Dia", icon: Calendar, component: WeekdayAnalysis },
  ];

  // aqui calculamos os próximos e anteriores índices dos slides. O módulo vai garantir que ao chegar no ultimo slide, ele volte
  // ao primeiro ao invés de tentar acessar um índice inexistente.
  const nextSlide = () => setCurrentSlide((prev) => (prev + 1) % slides.length);
  // vamos calcular o índice anterior de forma circular e o módulo vai garantir que voltemos ao final caso estejamos no comeco
  const prevSlide = () => setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);

  const CurrentComponent = slides[currentSlide].component;
  const CurrentIcon = slides[currentSlide].icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      {/* header */}
      <header className="border-b border-border/50 backdrop-blur-sm bg-card/30 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Analytics Dashboard</h1>
                <p className="text-sm text-muted-foreground">Análise de vendas em tempo real</p>
              </div>
            </div>
            
            {/* pontos de navegacão */}
            <div className="flex gap-2">
              {slides.map((slide) => (
                <button
                  key={slide.id}
                  onClick={() => setCurrentSlide(slide.id)}
                  className={`w-2 h-2 rounded-full transition-all ${
                    currentSlide === slide.id
                      ? "bg-primary w-8"
                      : "bg-muted-foreground/30 hover:bg-muted-foreground/50"
                  }`}
                  aria-label={`Ir para ${slide.title}`}
                />
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* conteúdo principal */}
      <main className="container mx-auto px-4 py-8">
        <div className="relative">
          {/* navegação do slide */}
          <div className="flex items-center justify-between mb-6">
            <Button
              variant="outline"
              size="icon"
              onClick={prevSlide}
              className="glass-card hover:bg-primary/10"
            >
              <ChevronLeft className="w-5 h-5" />
            </Button>

            <div className="flex items-center gap-3">
              <CurrentIcon className="w-6 h-6 text-primary" />
              <h2 className="text-3xl font-bold">{slides[currentSlide].title}</h2>
            </div>

            <Button
              variant="outline"
              size="icon"
              onClick={nextSlide}
              className="glass-card hover:bg-primary/10"
            >
              <ChevronRight className="w-5 h-5" />
            </Button>
          </div>

          {/* slide atual */}
          <div className="animate-fade-in">
            <CurrentComponent /> 
          </div>
        </div>
      </main>

      {/* footer */}
      <footer className="border-t border-border/50 mt-16 py-6 bg-card/30">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>Dashboard Analytics • Navegue usando as setas ou clique nos indicadores</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
