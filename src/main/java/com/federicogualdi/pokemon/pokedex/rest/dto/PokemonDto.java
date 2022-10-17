package com.federicogualdi.pokemon.pokedex.rest.dto;


import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class PokemonDto {
    private final String name;
    private final String description;
    private final String habitat;
    private final Boolean isLegendary;

    public static class Builder {
        private String name;
        private String description;
        private String habitat;
        private Boolean isLegendary;

        public PokemonDto.Builder name(String value) {
            name = value;
            return this;
        }

        public PokemonDto.Builder description(String value) {
            description = value;
            return this;
        }

        public PokemonDto.Builder habitat(String value) {
            habitat = value;
            return this;
        }

        public PokemonDto.Builder isLegendary(Boolean value) {
            isLegendary = value;
            return this;
        }

        public PokemonDto build() {
            return new PokemonDto(this);
        }
    }

    public PokemonDto(PokemonDto.Builder builder) {
        name = builder.name;
        description = builder.description;
        habitat = builder.habitat;
        isLegendary = builder.isLegendary;
    }

    public static PokemonDto clone(PokemonDto pokemon) {
        return new PokemonDto.Builder()
                .name(pokemon.getName())
                .description(pokemon.getDescription())
                .habitat(pokemon.getHabitat())
                .isLegendary(pokemon.isLegendary())
                .build();
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public String getHabitat() {
        return habitat;
    }

    @JsonProperty("isLegendary")
    public Boolean isLegendary() {
        return isLegendary;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PokemonDto that = (PokemonDto) o;
        return Objects.equals(name, that.name) && Objects.equals(description, that.description) && Objects.equals(habitat, that.habitat) && Objects.equals(isLegendary, that.isLegendary);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, description, habitat, isLegendary);
    }

    @Override
    public String toString() {
        return "PokemonDto{" + "name='" + name + '\'' + ", description='" + description + '\'' + ", habitat='" + habitat + '\'' + ", isLegendary=" + isLegendary + '}';
    }
}


