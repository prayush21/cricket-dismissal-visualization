"use client";

import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ScriptableContext,
} from "chart.js";
import { api } from "./api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

type PlayerStats = {
  max_runs_scored: number | null;
  dismissals_on_ball: { [key: string]: number };
  dismissals_on_run: { [key: string]: number };
  matches_played: number | null;
};

const CricketDashboard = () => {
  const [format, setFormat] = useState("ODI");
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [playerStats, setPlayerStats] = useState<PlayerStats | null>(null);

  useEffect(() => {
    fetchTeams();
  }, [format]);

  useEffect(() => {
    if (selectedTeam) {
      fetchPlayers();
    }
  }, [selectedTeam]);

  useEffect(() => {
    if (selectedPlayer) {
      fetchPlayerStats();
    }
  }, [selectedPlayer]);

  const fetchTeams = async () => {
    try {
      const response = await api.get(`/api/v2/teams?format=${format}`);
      setTeams(response.data);
      setSelectedTeam("");
      setPlayers([]);
      setSelectedPlayer("");
      setPlayerStats(null);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const response = await api.get(
        `/api/v2/players?format=${format}&team=${selectedTeam}`
      );
      setPlayers(response.data);
      setSelectedPlayer("");
      setPlayerStats(null);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  const fetchPlayerStats = async () => {
    try {
      const response = await api.get(
        `/api/v2/player-stats?format=${format}&player=${selectedPlayer}`
      );
      setPlayerStats(response.data);
    } catch (error) {
      setPlayerStats(null);
      console.error("Error fetching player stats:", error);
    }
  };

  const createChartData = (data: { [key: string]: number }, label: string) => {
    return {
      labels: Object.keys(data),
      datasets: [
        {
          label,
          data: Object.values(data),
          fill: true,
          backgroundColor: (context: ScriptableContext<"line">) => {
            const ctx = context.chart.ctx;
            const gradient = ctx.createLinearGradient(0, 0, 0, 200);
            gradient.addColorStop(0, "rgba(75, 192, 192, 0.6)");
            gradient.addColorStop(1, "rgba(75, 192, 192, 0.1)");
            return gradient;
          },
          borderColor: "rgba(75, 192, 192, 1)",
          pointBackgroundColor: "rgba(255, 255, 255, 1)",
          tension: 0.4,
        },
      ],
    };
  };

  const createRunChartData = (
    data: { [key: string]: number },
    label: string
  ) => {
    return {
      labels: Object.keys(data),
      datasets: [
        {
          label,
          data: Object.values(data),
          fill: true,
          backgroundColor: (context: ScriptableContext<"line">) => {
            const ctx = context.chart.ctx;
            const gradient = ctx.createLinearGradient(0, 0, 0, 200);
            gradient.addColorStop(0, "rgba(255, 99, 132, 0.6)");
            gradient.addColorStop(1, "rgba(255, 99, 132, 0.1)");
            return gradient;
          },
          borderColor: "rgba(255, 99, 132, 1)",
          pointBackgroundColor: "rgba(255, 255, 255, 1)",
          tension: 0.4,
        },
      ],
    };
  };

  const chartOptions = (titleText: string) => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
        labels: {
          color: "#E5E7EB",
          font: {
            size: 14,
          },
        },
      },
      title: {
        display: true,
        text: titleText,
        color: "#F3F4F6",
        font: {
          size: 20,
        },
      },
    },
    scales: {
      x: {
        ticks: { color: "#D1D5DB" },
        grid: { color: "rgba(255, 255, 255, 0.1)" },
      },
      y: {
        ticks: { color: "#D1D5DB" },
        grid: { color: "rgba(255, 255, 255, 0.1)" },
      },
    },
  });

  return (
    <div className="min-h-screen bg-background text-foreground p-4 sm:p-6 lg:p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-extrabold text-center">
          Tera Cricket Dashboard
        </h1>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Filters</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label>Format</Label>
                <Tabs value={format} onValueChange={setFormat}>
                  <TabsList>
                    <TabsTrigger value="ODI">ODI</TabsTrigger>
                    <TabsTrigger value="T20">T20</TabsTrigger>
                    <TabsTrigger value="IPL">IPL</TabsTrigger>
                  </TabsList>
                </Tabs>
              </div>

              <div>
                <Label>Team</Label>
                <Select value={selectedTeam} onValueChange={setSelectedTeam}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a team" />
                  </SelectTrigger>
                  <SelectContent>
                    {teams.map((team) => (
                      <SelectItem key={team} value={team}>
                        {team}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Player</Label>
                <Select
                  value={selectedPlayer}
                  onValueChange={setSelectedPlayer}
                  disabled={!selectedTeam}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select a player" />
                  </SelectTrigger>
                  <SelectContent>
                    {players.map((player) => (
                      <SelectItem key={player} value={player}>
                        {player}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              {/* <div>
                <Label>Date Range</Label>
                <DatePicker />
              </div> */}
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle>Player Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              {selectedPlayer && playerStats ? (
                <div>
                  <Tabs defaultValue="ball">
                    <TabsList>
                      <TabsTrigger value="ball">Dismissals by Ball</TabsTrigger>
                      <TabsTrigger value="run">Dismissals by Run</TabsTrigger>
                    </TabsList>
                    <TabsContent value="ball">
                      <div className="relative h-[300px] sm:h-[400px]">
                        <Line
                          data={createChartData(
                            playerStats.dismissals_on_ball,
                            "Dismissal Counts by Ball"
                          )}
                          options={chartOptions(
                            `Dismissal Analysis for ${selectedPlayer} (${format})`
                          )}
                        />
                      </div>
                    </TabsContent>
                    <TabsContent value="run">
                      <div className="relative h-[300px] sm:h-[400px]">
                        <Line
                          data={createRunChartData(
                            playerStats.dismissals_on_run,
                            "Dismissal Counts by Run"
                          )}
                          options={chartOptions(
                            `Dismissal Analysis for ${selectedPlayer} (${format})`
                          )}
                        />
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>
              ) : (
                <div className="flex items-center justify-center h-[300px] sm:h-[400px]">
                  <p className="text-2xl text-muted-foreground">
                    Select a player to see stats
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default CricketDashboard;
