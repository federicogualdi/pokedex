package com.federicogualdi.pokemon.pokedex.rest.dto;


import java.util.Objects;

public class PokemonDto {
    public String name;
    public String description;
    public String habitat;
    public Boolean isLegendary;

    public PokemonDto() {
    }

    public static PokemonDto Clone(PokemonDto pokemon) {
        var pokemonNew = new PokemonDto();
        pokemonNew.name = pokemon.name;
        pokemonNew.description = pokemon.description;
        pokemonNew.habitat = pokemon.habitat;
        pokemonNew.isLegendary = pokemon.isLegendary;
        return pokemonNew;
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


